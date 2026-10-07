import streamlit as st
from google import genai
from google.genai import types
from PIL import Image


st.set_page_config(
    page_title="CyberShield",
    page_icon="🛡️",
    layout="centered",
)


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error(
        "No se encontró GEMINI_API_KEY en "
        ".streamlit/secrets.toml"
    )
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL = "gemini-2.5-flash"


# ----------------------------------------------------------------------
# UI
# ----------------------------------------------------------------------

st.title("🛡️ CyberShield")
st.subheader("Tu asistente de seguridad digital")

st.write(
    "Sube una captura de pantalla y CyberShield analizará "
    "posibles señales de phishing, fraude, malware o "
    "ingeniería social."
)

st.warning(
    "⚠️ No subas contraseñas, códigos de autenticación, "
    "números completos de tarjetas ni otra información "
    "confidencial."
)


uploaded_file = st.file_uploader(
    "📸 Sube una captura de pantalla",
    type=["png", "jpg", "jpeg", "webp"],
)


if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Captura seleccionada",
        use_container_width=True,
    )

    if st.button(
        "🔍 Analizar captura",
        type="primary",
        use_container_width=True,
    ):

        prompt = """
Eres CyberShield, un asistente especializado en
ciberseguridad para usuarios comunes.

Analiza cuidadosamente la imagen proporcionada.

Tu objetivo es identificar señales visibles de:

- phishing
- estafas
- ingeniería social
- sitios web fraudulentos
- mensajes sospechosos
- malware
- descargas potencialmente peligrosas
- solicitudes sospechosas de credenciales
- solicitudes de códigos de autenticación
- fraude bancario
- suplantación de identidad

REGLAS IMPORTANTES:

1. Analiza únicamente la información visible en la imagen.
2. No inventes información que no aparezca en ella.
3. Si algo no puede determinarse, dilo claramente.
4. No afirmes que algo es malicioso con certeza si solamente
   existen indicios.
5. Explica el riesgo en lenguaje sencillo.
6. Si existe una acción urgente que el usuario debería realizar,
   indícala claramente.
7. Nunca solicites al usuario que proporcione contraseñas,
   códigos MFA, números completos de tarjetas u otra información
   confidencial.

Devuelve el resultado utilizando exactamente esta estructura:

## Nivel de riesgo

Indica uno de:

🟢 BAJO
🟡 PRECAUCIÓN
🟠 ALTO
🔴 CRÍTICO

## Resumen

Explica brevemente qué observaste.

## Señales detectadas

Lista las señales sospechosas que realmente sean visibles
en la imagen.

## ¿Qué podría estar ocurriendo?

Explica el escenario probable, dejando claro el nivel de certeza.

## Qué debes hacer

Proporciona una lista concreta de acciones que debería realizar
el usuario.

## Qué NO debes hacer

Proporciona una lista de acciones que el usuario debería evitar.

## Confianza del análisis

Indica:

Alta, Media o Baja

y explica brevemente por qué.

Recuerda: una captura de pantalla puede no contener suficiente
información para determinar si algo es legítimo o malicioso.
En ese caso, dilo explícitamente.
"""

        with st.spinner("🛡️ CyberShield está analizando la captura..."):

            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=[
                        types.Part.from_bytes(
                            data=uploaded_file.getvalue(),
                            mime_type=uploaded_file.type,
                        ),
                        prompt,
                    ],
                )

                st.divider()

                st.header("🛡️ Resultado del análisis")

                st.markdown(response.text)

            except Exception as exc:

                st.error(
                    "Ocurrió un error al analizar la imagen."
                )

                st.exception(exc)