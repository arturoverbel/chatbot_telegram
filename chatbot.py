import params_func
import results
import answer
import read
import config
import logs


def run_chatbot():

    config.set_run_forever_again()

    while(config.validate_run_forever()):

        # Leer mensajes
        datas = read.update()
        # Setiar funciones en el sistema, nombres, archivos,..
        params_func.set_params(datas)
        # Envia cuestionario
        answer.send_answers()

    # Ejecuta reporte
    results.export_results()
    logs.clean()


def stop_chatbot():
    return config.stop_forever()
