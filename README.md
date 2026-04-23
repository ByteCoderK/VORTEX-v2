# V.O.R.T.E.X.

**Voice-Operated Reactive Technology for Extreme eXecution**

VORTEX is a Python-based AI automation system that connects conversational intelligence, command routing, scheduled routines, cloud hosting, and ESP8266-powered device control into one assistant backend.

The project is designed as more than a chatbot. It acts as a control layer between user intent and real-world execution: accepting commands, routing them through an AI core, scheduling device actions, calling APIs, and controlling physical relays over MQTT.

---

## Overview

VORTEX is built around a modular assistant architecture:

- A **FastAPI backend** exposes assistant endpoints for remote access.
- A **Neural Core** sends user prompts to an external AI worker and enforces structured JSON responses.
- A **Router** processes commands, calls the AI layer, detects routines, and reloads scheduled jobs.
- A **Routine Engine** stores, schedules, and executes time-based automation.
- An **MQTT automation layer** sends relay commands to an ESP8266 controller.
- An **Arduino/ESP8266 firmware module** receives MQTT messages and controls four hardware relays.

This makes VORTEX suitable for smart-room control, voice-driven automation, hosted assistant workflows, and custom AI-powered command execution.

---

## Core Capabilities

### AI Command Processing

VORTEX uses `core/NeuralCore.py` to send prompts, system instructions, and conversation history to an external AI endpoint. The core expects structured JSON responses containing:

- Assistant response text
- Tone metadata
- Device action instructions
- New long-term memory entries

The system includes retry handling and fallback worker support through a secondary AI endpoint.

### Command Routing

`router/router.py` acts as the main decision layer. It receives a query, runs AI processing, attempts routine parsing, stores valid routines, and reloads the scheduler when new automation is detected.

The router also supports direct command hooks, such as weather lookup.

### Smart Device Control

VORTEX controls four device channels through MQTT:

| Relay | Device |
| --- | --- |
| 1 | Light |
| 2 | Wind / Fan |
| 3 | Ambient |
| 4 | Socket / Plug |

Device commands are sent through `commands/XAUTOMATION.py` using secure MQTT over port `8883`.

### ESP8266 Relay Firmware

The `X12E-AUTOMATION/X12E-AUTOMATION.ino` sketch connects an ESP8266 board to Wi-Fi and MQTT. It listens for command values and switches four relay pins accordingly.

The Python backend publishes compact command codes, and the ESP8266 translates them into relay ON/OFF states.

### Routine Scheduling

The routines system allows natural-language scheduling such as:

```text
turn on light at 7:30 pm every day
turn off socket at 11 pm
turn on fan at 06:00 every monday
```

Routine modules:

- `routines/routine_parser.py` extracts time, frequency, device, relay, and state.
- `routines/routine_db.py` persists routines in SQLite.
- `routines/routine_engine.py` registers jobs using the `schedule` library.
- `routines/routine_executor.py` executes scheduled actions through the ESP controller.

Routine times are stored in IST and converted to UTC for cloud-hosted scheduling environments.

### Hosted API

`vortex_api.py` exposes the assistant through FastAPI.

Available endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` / `POST` | `/ping` | Health check |
| `POST` | `/ask` | Submit a user query |
| `GET` | `/stream_logs` | Stream backend logs through Server-Sent Events |

The API also includes a Render keep-alive task that periodically calls the configured deployment URL.

### Weather Lookup

`commands/Weather.py` integrates with OpenWeatherMap and can fetch:

- Weather description
- Temperature
- Humidity
- Wind speed

---

## Tech Stack

- **Python 3.11**
- **FastAPI**
- **Uvicorn**
- **HTTPX**
- **Requests**
- **Paho MQTT**
- **SQLite**
- **Schedule**
- **ESP8266 / Arduino C++**
- **OpenWeatherMap API**
- **Render-compatible deployment**

---

## Project Structure

```text
VORTEX-v2/
├── commands/
│   ├── Weather.py
│   └── XAUTOMATION.py
├── core/
│   └── NeuralCore.py
├── router/
│   └── router.py
├── routines/
│   ├── devices.py
│   ├── routine_db.py
│   ├── routine_engine.py
│   ├── routine_executor.py
│   └── routine_parser.py
├── X12E-AUTOMATION/
│   └── X12E-AUTOMATION.ino
├── VORTEX.py
├── vortex_api.py
├── requirements.txt
├── runtime.txt
└── README.md
```

---

## Environment Variables

Configure these values in your hosting environment, terminal session, or process manager. The `.env.example` file documents the expected variable names.

Required variables include:

```env
url=
url_2=
API_KEY=
weather_api_ley=
broker=
username=
password=
topic_cmd=
topic_feedback=
topic_cmd_2=
topic_feedback_2=
render_url=
render_ask=
```

### Variable Reference

| Variable | Purpose |
| --- | --- |
| `url` | Primary AI worker endpoint |
| `url_2` | Fallback AI worker endpoint |
| `API_KEY` | Authorization token for the AI worker |
| `weather_api_ley` | OpenWeatherMap API key |
| `broker` | MQTT broker host |
| `username` | MQTT username |
| `password` | MQTT password |
| `topic_cmd` | MQTT command topic for router control |
| `topic_feedback` | MQTT feedback topic for router control |
| `topic_cmd_2` | MQTT command topic for routine/device module |
| `topic_feedback_2` | MQTT feedback topic for routine/device module |
| `render_url` | Render deployment URL used by keep-alive |
| `render_ask` | Hosted `/ask` endpoint used by the CLI client |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/VORTEX.git
cd VORTEX
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Set the required variables before starting the backend. On Render, add them through the service environment settings. For local development, export them in your shell or load them through your preferred environment manager.

---

## Running Locally

Start the FastAPI backend:

```bash
uvicorn vortex_api:app --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/ping
```

Send a query:

```bash
curl -X POST http://localhost:8000/ask -H "Content-Type: application/json" -d "{\"query\":\"turn on light at 7:30 pm every day\"}"
```

Run the CLI client:

```bash
python VORTEX.py
```

---

## API Usage

### `POST /ask`

Request:

```json
{
  "query": "turn on light at 7:30 pm every day"
}
```

Response:

```json
{
  "ATLAS": "Routine saved."
}
```

### `GET /stream_logs`

Streams `vortex_debug.log` using Server-Sent Events. This is useful for monitoring hosted execution, routine scheduling, and command routing behavior.

---

## Hardware Automation

The ESP8266 firmware controls four relay channels.

Default relay pin mapping:

| Relay | GPIO |
| --- | --- |
| Relay 1 | GPIO 5 |
| Relay 2 | GPIO 4 |
| Relay 3 | GPIO 14 |
| Relay 4 | GPIO 12 |

MQTT command mapping:

| Command | Action |
| --- | --- |
| `1` | Relay 1 ON |
| `2` | Relay 1 OFF |
| `3` | Relay 2 ON |
| `4` | Relay 2 OFF |
| `5` | Relay 3 ON |
| `6` | Relay 3 OFF |
| `7` | Relay 4 ON |
| `8` | Relay 4 OFF |

The firmware uses `WiFiClientSecure` and `PubSubClient` to connect to the broker.

---

## Deployment

VORTEX is designed to run on Render or any platform capable of hosting a Python FastAPI service.

The included `runtime.txt` targets:

```text
python-3.11.11
```

Recommended Render start command:

```bash
uvicorn vortex_api:app --host 0.0.0.0 --port $PORT
```

The API includes a keep-alive coroutine that pings the configured `render_url` every 840 seconds.

---

## Security Notes

VORTEX can trigger real-world device actions and communicate with external AI and MQTT services. Treat deployment security seriously.

Recommended precautions:

- Keep `.env` out of version control.
- Rotate exposed MQTT or API credentials immediately.
- Do not expose command execution endpoints without authentication.
- Validate commands before connecting them to sensitive devices.
- Use separate MQTT topics for testing and production.
- Avoid running the backend with unnecessary system privileges.

---

## Known Limitations

- Voice input is expected to be handled by a client layer; the current backend accepts text queries.
- Weather output currently prints data instead of returning a clean structured response.
- Routine parsing is rule-based and optimized for simple time/device commands.
- ESP8266 firmware credentials are currently hardcoded placeholders and should be moved to a safer configuration method before production use.
- The assistant response contract depends on the external AI worker returning valid JSON.
- Local `.env` files are documented, but the current code reads process environment variables directly.

---

## Roadmap

- Voice client integration
- Stronger routine parsing with NLP support
- Routine management endpoints
- Authentication for hosted API access
- Structured weather responses
- Device status feedback dashboard
- Improved memory storage
- Spotify and media controls
- Telegram or Discord bot bridge
- Browser and desktop automation modules
- More robust ESP feedback handling

---

## License

This project is proprietary.

Redistribution, modification, or commercial use is not permitted without explicit written permission from the author.

For commercial inquiries, collaboration requests, or licensing discussions, contact:

**alvyu.official@gmail.com**

---

## Author

Developed and maintained by **Alvyu**.

VORTEX represents years of experimentation across AI assistants, automation systems, cloud deployment, MQTT communication, and physical device control.
