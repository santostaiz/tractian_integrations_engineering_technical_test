# """Entrypoint for the application."""

# import asyncio


# async def main():
#     print("Hello, World!")


# if __name__ == "__main__":
#     asyncio.run(main())

from src.config import DATA_INBOUND_DIR, DATA_OUTBOUND_DIR
from src.tracOS.repository import TracOSRepository
from src.client.reader import load_client_workorders, write_client_workorder
from src.translator.mapping import client_to_tracos, tracos_to_client
from src.logger import logger

def run_inbound(repo: TracOSRepository):
    logger.info("Iniciando fluxo de entrada (Inbound)...")
    workorders = load_client_workorders(DATA_INBOUND_DIR)
    for raw in workorders:
        try:
            normalized = client_to_tracos(raw)
            repo.upsert_workorder(normalized)
            logger.info(f"Ordem de serviço {normalized['id']} sincronizada com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao processar ordem de serviço: {e}")

def run_outbound(repo: TracOSRepository):
    logger.info("Iniciando fluxo de saída (Outbound)...")
    unsynced = repo.get_unsynced_workorders()
    for wo in unsynced:
        try:
            client_format = tracos_to_client(wo)
            write_client_workorder(DATA_OUTBOUND_DIR, f"{wo['id']}.json", client_format)
            repo.mark_as_synced(wo["id"])
            logger.info(f"Ordem {wo['id']} exportada e marcada como sincronizada.")
        except Exception as e:
            logger.error(f"Erro ao exportar ordem {wo['id']}: {e}")

if __name__ == "__main__":
    repo = TracOSRepository()
    run_inbound(repo)
    run_outbound(repo)
