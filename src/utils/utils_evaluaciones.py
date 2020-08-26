import src.validaciones_json.constantes_json as jsonConst
from selenium.common.exceptions import TimeoutException
from src.webdriver_config import config_constantes
from src.utils.utils_temporizador import Temporizador
from src.utils.utils_format import FormatUtils
from src.utils.utils_main import UtilsMain
from src.webdriver_actions.html_actions import HtmlActions
from selenium.webdriver.remote.webdriver import WebDriver



class UtilsEvaluaciones:

    @staticmethod
    def finalizar_tiempos_en_step(jsonEval, indice: int ,tiempo_step_inicio, fecha_inicio):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
        jsonEval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][indice]["start"] = fecha_inicio
        jsonEval["steps"][indice]["end"] = fecha_fin

        return jsonEval


    @staticmethod
    def establecer_output_status_step(jsonEval, indice: int, sub_indice: int, paso_exitoso: bool, mensaje_output: str):

        status_del_step = jsonConst.SUCCESS if paso_exitoso else jsonConst.FAILED

        jsonEval["steps"][indice]["output"][sub_indice]["status"] = status_del_step
        jsonEval["steps"][indice]["status"] = status_del_step
        jsonEval["steps"][indice]["output"][sub_indice]["output"] = mensaje_output

        return jsonEval

    @staticmethod
    def generar_json_inicio_de_sesion_incorrecta(jsonEval, tiempo_step_inicio, fecha_inicio, indice: int,
                                                 msg_output: str):

        if tiempo_step_inicio is None:
            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

        jsonEval["steps"][indice]["output"][0]["status"] = jsonConst.FAILED
        jsonEval["steps"][indice]["status"] = jsonConst.FAILED
        jsonEval["steps"][indice]["output"][0]["output"] = msg_output

        tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
        fecha_fin = Temporizador.obtener_fecha_tiempo_actual()

        jsonEval["steps"][indice]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
        jsonEval["steps"][indice]["start"] = fecha_inicio
        jsonEval["steps"][indice]["end"] = fecha_fin

        return jsonEval

    @staticmethod
    def se_ingreso_correctamente_a_la_sesion(jsonEval):
        return True if jsonEval["steps"][1]["status"] == jsonConst.SUCCESS else False

    @staticmethod
    def verificar_descarga_en_ejecucion(nombre_del_archivo, extension_del_archivo):
        tiempo_inicio = Temporizador.obtener_tiempo_timer()
        se_descargo_el_archivo_exitosamente = False
        archivo_a_localizar = '{}{}'.format(nombre_del_archivo, extension_del_archivo)

        while (Temporizador.obtener_tiempo_timer() - tiempo_inicio) < 180:
            lista_archivos = UtilsMain.obtener_lista_ficheros_en_directorio(config_constantes.PATH_CARPETA_DESCARGA)

            if archivo_a_localizar in lista_archivos:
                se_descargo_el_archivo_exitosamente = True
                break

        if not se_descargo_el_archivo_exitosamente:
            raise TimeoutException(msg='Han transcurrido 3 minutos sin finalizar la descarga del archivo {} desde '
                                       'el portal Claro Drive'.format(archivo_a_localizar))
