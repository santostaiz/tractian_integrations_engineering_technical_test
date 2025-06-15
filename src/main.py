from src.config import get_data_inbound_dir, get_data_outbound_dir
from src.tracOS.repository import TracOSRepository
from src.client.reader import load_client_workorders
from src.client.writer import write_client_workorder
from src.translator.mapping import client_to_tracos, tracos_to_client
from src.logger import logger
import os

def run_inbound(repo: TracOSRepository):
    logger.info("Iniciando fluxo de entrada (Inbound)...")
    workorders = load_client_workorders(get_data_inbound_dir())
    workorders = sorted(workorders, key=lambda x: int(x["orderNo"]))
    if not workorders:
        logger.warning(f"Nenhuma ordem encontrada no diretório {get_data_inbound_dir()}")
   
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
    unsynced = sorted(unsynced, key=lambda x: int(x["id"]))
    if not unsynced:
        logger.info("Nenhuma ordem pendente para sincronização.")

    for wo in unsynced:
        try:
            client_format = tracos_to_client(wo)
            write_client_workorder(get_data_outbound_dir(), f"{wo['id']}.json", client_format)
            repo.mark_as_synced(wo["id"])
            logger.info(f"Ordem {wo['id']} exportada e marcada como sincronizada.")
        except Exception as e:
            logger.error(f"Erro ao exportar ordem {wo['id']}: {e}")

if __name__ == "__main__":
    logger.info("Pipeline de integração iniciado")
    try:
        # Validação dos diretórios
        for directory in [get_data_inbound_dir(), get_data_outbound_dir()]:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Diretório {directory} criado.")

        # Conexão com MongoDB
        try:
            repo = TracOSRepository()
        except Exception as e:
            logger.critical(f"Falha ao conectar ao MongoDB: {e}")
            exit(1)

        # Execução dos fluxos
        run_inbound(repo)
        run_outbound(repo)

    except KeyboardInterrupt:
        logger.warning("Execução interrompida manualmente pelo usuário.")
    except Exception as e:
        logger.critical(f"Erro inesperado no pipeline: {e}")
    finally:
        logger.info("Pipeline de integração finalizado.")