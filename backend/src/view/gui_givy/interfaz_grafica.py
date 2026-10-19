from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import sys
sys.path.append("src")
from model import calculo, excepciones


class CalculadoraHipotecaInversa(App):

    def build(self):
        self.contenedor = BoxLayout(orientation='vertical', padding=10, spacing=10)


        self.contenedor.add_widget(Label(text="Edad:"))
        self.input_edad = TextInput(multiline=False)
        self.input_edad.size_hint = (1, None)
        self.input_edad.height = 40
        self.contenedor.add_widget(self.input_edad)


        self.contenedor.add_widget(Label(text="Valor de la vivienda:"))
        self.input_valor = TextInput(multiline=False)
        self.input_valor.size_hint = (1, None)
        self.input_valor.height = 40
        self.contenedor.add_widget(self.input_valor)


        boton_calcular = Button(text="Calcular")
        boton_calcular.bind(on_press=self.calcular)
        self.contenedor.add_widget(boton_calcular)


        self.resultados = Label(text="")
        self.contenedor.add_widget(self.resultados)


        self.input_edad.focus = True

        return self.contenedor

    def calcular(self, instance):
        errores = []

        edad_texto = self.input_edad.text.strip()
        valor_texto = self.input_valor.text.strip()

        edad = None
        valor_vivienda = None

        # --- Validar edad ---
        if not edad_texto:
            errores.append("El campo 'Edad' está vacío.")
        else:
            try:
                edad = int(edad_texto)
            except ValueError:
                errores.append("El campo 'Edad' debe ser un número entero válido.")
            else:
                # Validación de reglas personalizadas para edad
                try:
                    calculo.calcular_porcentaje_financiado(edad)
                except excepciones.ExcepcionPorEdadIncorrectaNegativa as e:
                    errores.append(str(e))
                except excepciones.ExcepcionPorEdadIncorrectaMenorAMinimina as e:
                    errores.append(str(e))
                except excepciones.ExcepcionPorEdadIncorrectaMayorAMaxima as e:
                    errores.append(str(e))
                except excepciones.ExcepcionPorEdadIncorrectaDecimal as e:
                    errores.append(str(e))
                except excepciones.ExcepcionPorEdadIncorrectaNoNumerica as e:
                    errores.append(str(e))

        # --- Validar valor de vivienda ---
        if not valor_texto:
            errores.append("El campo 'Valor de la vivienda' está vacío.")
        else:
            try:
                valor_vivienda = float(valor_texto)
            except ValueError:
                errores.append("El campo 'Valor de la vivienda' debe ser un número válido.")
            else:
                try:
                    calculo.verificar_valor_vivienda(valor_vivienda)
                except excepciones.ExcepcionPorValorViviendaInvalido as e:
                    errores.append(str(e))

        # --- Mostrar errores si hay ---
        if errores:
            mensaje = "\n".join(errores)
            self.mostrar_popup("Errores en el formulario", mensaje)
            return

        # --- Si no hay errores, ejecutar cálculo completo ---
        porcentaje_financiado = calculo.calcular_porcentaje_financiado(edad)
        plazo_anios = calculo.calcular_plazo_financiacion(edad)
        pago_mensual = calculo.calcular_pago_mensual(
            porcentaje_financiado,
            valor_vivienda,
            plazo_anios
        )
        intereses_totales, saldo_final = calculo.calcular_intereses(
            pago_mensual,
            calculo.TASA_EFECTIVA_MENSUAL,
            plazo_anios
        )

        self.resultados.text = (
            f"Porcentaje financiado: {porcentaje_financiado}%\n"
            f"Plazo en años: {plazo_anios}\n"
            f"Pago mensual: ${pago_mensual:,.2f}\n"
            f"Intereses Totales: ${intereses_totales:,.2f}\n"
            f"Saldo Final: ${saldo_final:,.2f}"
        )

    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup

    def mostrar_popup(self, titulo, mensaje):
        # Contenedor para centrar el label
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        label = Label(
            text=mensaje,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            text_size=(0.8 * self.contenedor.width, None)  # ajusta el texto al ancho
        )
        label.bind(texture_size=label.setter('size'))  # ajusta el tamaño del label

        layout.add_widget(label)

        popup = Popup(
            title=titulo,
            content=layout,
            size_hint=(0.9, None),
            height=350,
            auto_dismiss=True
        )
        popup.open()


if __name__ == "__main__":
    CalculadoraHipotecaInversa().run()


