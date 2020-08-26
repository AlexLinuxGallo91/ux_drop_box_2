import time
from os import path
from pathlib import Path

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.step_evaluaciones import constantes_evaluaciones_claro_drive
from src.utils.utils_evaluaciones import UtilsEvaluaciones
from src.utils.utils_format import FormatUtils
from src.utils.utils_html import ValidacionesHtml
from src.utils.utils_temporizador import Temporizador


class EvaluacionesDropBoxDriveSteps:

    def ingreso_pagina_principal_dropbox(self, webdriver_test_ux: WebDriver, json_eval, url_login):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            webdriver_test_ux.get(url_login)

            WebDriverWait(webdriver_test_ux, 10).until(
                EC.presence_of_element_located((By.NAME, 'login_email')))

            WebDriverWait(webdriver_test_ux, 10).until(
                EC.presence_of_element_located((By.NAME, 'login_password')))

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 0, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 0 ,tiempo_step_inicio, fecha_inicio)

        return json_eval


    def inicio_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, url_login):
        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:

            btn_inicio_sesion = WebDriverWait(webdriver_test_ux, 6).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="auth-google button-primary"]')))
            btn_inicio_sesion.click()

            if ValidacionesHtml.se_encuentran_mas_ventanas_en_sesion(webdriver_test_ux, 6):
                ventana_padre = webdriver_test_ux.window_handles[0]
                ventana_hija = webdriver_test_ux.window_handles[1]

                webdriver_test_ux.switch_to.window(ventana_hija)

            modo_no_grafico = FormatUtils.lector_archivo_ini().getboolean('Driver', 'headless')

            if modo_no_grafico:
                input_correo_gmail = WebDriverWait(webdriver_test_ux, 6).until(
                    EC.element_to_be_clickable((By.ID, 'Email')))
                input_correo_gmail.send_keys(json_args['user'])

                btn_next_gmail_sec_email = WebDriverWait(webdriver_test_ux, 6).until(
                    EC.element_to_be_clickable((By.ID, 'next')))
                btn_next_gmail_sec_email.click()

                input_pass_gmail = WebDriverWait(webdriver_test_ux, 60).until(
                    EC.presence_of_element_located((By.ID, 'password')))
                input_pass_gmail.send_keys(json_args['password'])

                btn_next_gmail_sec_password = WebDriverWait(webdriver_test_ux, 6).until(
                    EC.element_to_be_clickable((By.ID, 'submit')))
                btn_next_gmail_sec_password.click()

            else:

                input_correo_gmail = WebDriverWait(webdriver_test_ux, 10).until(
                    EC.presence_of_element_located((By.ID, 'identifierId')))

                WebDriverWait(webdriver_test_ux, 10).until(
                    EC.element_to_be_clickable((By.ID, 'identifierId')))

                input_correo_gmail.click()
                input_correo_gmail.send_keys(json_args['user'])

                btn_next_gmail_sec_email = WebDriverWait(webdriver_test_ux, 10).until(
                    EC.presence_of_element_located((By.ID, 'identifierNext')))

                WebDriverWait(webdriver_test_ux, 10).until(
                    EC.element_to_be_clickable((By.ID, 'identifierNext')))

                btn_next_gmail_sec_email.click()

                div_form = WebDriverWait(webdriver_test_ux, 10).until(
                    EC.presence_of_element_located((By.ID, 'password')))

                input_pass_gmail = WebDriverWait(div_form, 10).until(
                    EC.presence_of_element_located((By.NAME, 'password')))

                input_pass_gmail.click()
                input_pass_gmail.send_keys(json_args['password'])

                btn_next_gmail_sec_password = WebDriverWait(webdriver_test_ux, 10).until(
                    EC.element_to_be_clickable((By.ID, 'passwordNext')))
                btn_next_gmail_sec_password.click()

            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            webdriver_test_ux.switch_to.window(ventana_padre)

            WebDriverWait(webdriver_test_ux, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'maestro-nav__contents')))

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 1, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 1, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, nombre_archivo_sin_ext,
                               nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)
            ValidacionesHtml.verificar_archivo_ya_existente_en_portal(webdriver_test_ux, nombre_archivo_sin_ext)

            input_carga_de_archivo = WebDriverWait(webdriver_test_ux, 10).until(
                EC.presence_of_element_located((By.XPATH, '//body/div/div/input[1]')))

            input_carga_de_archivo.send_keys(json_args['pathImage'])

            WebDriverWait(webdriver_test_ux, 12).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="ReactModal__Content '
                                                          'ReactModal__Content--after-open dig-Modal folder-picker-modal"]')))

            btn_cargar = WebDriverWait(webdriver_test_ux, 12).until(EC.visibility_of_element_located(
                (By.XPATH, '//button[@class="dig-Button dig-Button--primary dig-Button--standard"]')))

            WebDriverWait(webdriver_test_ux, 12).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'folder-picker__empty-message')))

            btn_cargar.click()

            WebDriverWait(webdriver_test_ux, 720).until(EC.presence_of_element_located(
                (By.XPATH,
                 '//p[@class="mc-snackbar-title"][text()="Se carg\u00F3 {}."]'.format(nombre_archivo_con_ext))))


            btn_cerrar_progreso_carga = WebDriverWait(webdriver_test_ux, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//span[@class="mc-button-content"][text()="Cerrar"]')))

            btn_cerrar_progreso_carga.click()

            webdriver_test_ux.refresh()

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 2, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 2, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def descargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):

        extension_del_archivo = path.splitext(nombre_archivo_con_ext)[1]
        nombre_del_archivo_sin_extension = Path(nombre_archivo_con_ext).stem

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)

            search_bar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'search__input')))

            search_bar.send_keys(nombre_archivo_con_ext)
            time.sleep(1)
            search_bar.send_keys(Keys.RETURN)

            archivo_por_descargar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//tr[@data-filename="{}"]'.format(nombre_archivo_con_ext))))

            btn_mas_acciones = WebDriverWait(archivo_por_descargar, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'browse-overflow-menu')))

            btn_mas_acciones.click()

            btn_descargar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'action-download')))

            btn_descargar.click()

            UtilsEvaluaciones.verificar_descarga_en_ejecucion(nombre_del_archivo_sin_extension, extension_del_archivo)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 3, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 3, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def eliminar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:

            archivo_por_descargar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//tr[@data-filename="{}"]'.format(nombre_archivo_con_ext))))

            btn_mas_acciones = WebDriverWait(archivo_por_descargar, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'browse-overflow-menu')))

            btn_mas_acciones.click()

            btn_eliminar = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'action-delete')))

            btn_eliminar.click()

            btn_eliminar_modal = WebDriverWait(webdriver_test_ux, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//span[@class="mc-button-content"][text()="Eliminar"]')))

            btn_eliminar_modal.click()

            WebDriverWait(webdriver_test_ux, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//p[@class="mc-snackbar-title"][text()="Se elimin\u00F3 1 elemento."]')))

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 4, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 4, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cerrar_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            boton_imagen_perfil = WebDriverWait(webdriver_test_ux, 12).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'dig-Menu')))

            boton_imagen_perfil.click()

            boton_salir_sesion = WebDriverWait(webdriver_test_ux, 12).until(
                EC.element_to_be_clickable((By.XPATH, '//span[text()="Salir"]')))

            boton_salir_sesion.click()

            WebDriverWait(webdriver_test_ux, 12).until(EC.element_to_be_clickable((By.NAME, 'login_email')))

            WebDriverWait(webdriver_test_ux, 12).until(EC.element_to_be_clickable((By.NAME, 'login_password')))

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 5, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 5, tiempo_step_inicio, fecha_inicio)

        return json_eval
