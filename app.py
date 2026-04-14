from __future__ import annotations

import html
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

SPECIALTIES = [
    "Consulta general",
    "Vacunacion",
    "Control cachorro",
    "Dermatologia veterinaria",
    "Guardia felina",
]

APPOINTMENT_SLOTS = [
    {
        "id": "T001",
        "specialty": "Consulta general",
        "professional": "Dra. Paula Sosa",
        "date": "2026-04-15",
        "time": "09:00",
        "mode": "Presencial",
    },
    {
        "id": "T002",
        "specialty": "Vacunacion",
        "professional": "Dr. Martin Quiroga",
        "date": "2026-04-15",
        "time": "10:30",
        "mode": "Presencial",
    },
    {
        "id": "T003",
        "specialty": "Control cachorro",
        "professional": "Dra. Luciana Vera",
        "date": "2026-04-15",
        "time": "12:00",
        "mode": "Presencial",
    },
    {
        "id": "T004",
        "specialty": "Guardia felina",
        "professional": "Dr. Tomas Funes",
        "date": "2026-04-16",
        "time": "08:30",
        "mode": "Teleconsulta",
    },
    {
        "id": "T005",
        "specialty": "Dermatologia veterinaria",
        "professional": "Dra. Sofia Amaya",
        "date": "2026-04-16",
        "time": "16:00",
        "mode": "Teleconsulta",
    },
    {
        "id": "T006",
        "specialty": "Consulta general",
        "professional": "Dr. Federico Ledesma",
        "date": "2026-04-17",
        "time": "18:15",
        "mode": "Presencial",
    },
]

BOOKED_APPOINTMENTS: list[dict[str, str]] = []


def available_slots() -> list[dict[str, str]]:
    booked_ids = {appointment["slot_id"] for appointment in BOOKED_APPOINTMENTS}
    return [slot for slot in APPOINTMENT_SLOTS if slot["id"] not in booked_ids]


def find_slot(slot_id: str) -> dict[str, str] | None:
    for slot in APPOINTMENT_SLOTS:
        if slot["id"] == slot_id:
            return slot
    return None


def build_alert(message: str, kind: str) -> str:
    if not message:
        return ""
    return f'<div class="alert alert-{kind} shadow-sm" role="alert">{html.escape(message)}</div>'


def build_slot_cards() -> str:
    slots = available_slots()
    if not slots:
        return """
        <div class="col-12">
          <div class="empty-state">
            No hay turnos disponibles en este momento. Reinicia la app o agrega nuevos horarios al mock.
          </div>
        </div>
        """

    cards = []
    for slot in slots:
        cards.append(
            f"""
            <div class="col-12 col-md-6 col-xl-4">
              <article class="slot-card h-100">
                <div class="slot-badge">{html.escape(slot["specialty"])}</div>
                <h3>{html.escape(slot["professional"])}</h3>
                <ul class="slot-list">
                  <li><i class="bi bi-calendar-event"></i> {html.escape(slot["date"])}</li>
                  <li><i class="bi bi-clock"></i> {html.escape(slot["time"])}</li>
                  <li><i class="bi bi-laptop"></i> {html.escape(slot["mode"])}</li>
                </ul>
                <a class="btn btn-primary w-100" href="#solicitar-turno" onclick="document.getElementById('slot_id').value='{html.escape(slot['id'])}'">
                  Solicitar este turno
                </a>
              </article>
            </div>
            """
        )
    return "".join(cards)


def build_slot_options(selected_slot: str) -> str:
    options = ['<option value="">Elegir turno disponible</option>']
    for slot in available_slots():
        label = f'{slot["specialty"]} | {slot["date"]} {slot["time"]} | {slot["professional"]}'
        selected = " selected" if slot["id"] == selected_slot else ""
        options.append(
            f'<option value="{html.escape(slot["id"])}"{selected}>{html.escape(label)}</option>'
        )
    return "".join(options)


def build_recent_requests() -> str:
    if not BOOKED_APPOINTMENTS:
        return """
        <div class="empty-state compact">
          Aun no se cargaron solicitudes. Usa el formulario para generar el primer turno.
        </div>
        """

    items = []
    for appointment in reversed(BOOKED_APPOINTMENTS[-5:]):
        slot = find_slot(appointment["slot_id"])
        if not slot:
            continue
        patient = appointment["patient_name"].split()[0]
        items.append(
            f"""
            <div class="request-item">
              <div>
                <strong>{html.escape(patient)}</strong>
                <span>{html.escape(slot["specialty"])} con {html.escape(slot["professional"])}</span>
              </div>
              <span class="request-time">{html.escape(slot["date"])} {html.escape(slot["time"])}</span>
            </div>
            """
        )
    return "".join(items)


def render_home(message: str = "", kind: str = "success", form_data: dict[str, str] | None = None) -> bytes:
    form_data = form_data or {}
    page = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Clinica Veterinaria Firulais</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <style>{STYLE_CSS}</style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg sticky-top app-nav">
      <div class="container">
        <a class="navbar-brand" href="/">Firulais</a>
        <div class="ms-auto d-flex gap-3 align-items-center">
          <a class="nav-link" href="#disponibles">Disponibles</a>
          <a class="btn btn-sm btn-primary" href="#solicitar-turno">Pedir turno</a>
        </div>
      </div>
    </nav>

    <header class="hero">
      <div class="container">
        <div class="row align-items-center g-4">
          <div class="col-12 col-xl-7">
            <span class="eyebrow">Clinica Veterinaria Firulais</span>
            <h1>Saca un turno para tu mascota de forma simple y rapida.</h1>
            <p class="hero-copy">
              Demo simple sin autenticacion para una veterinaria, con agenda publica y un flujo claro
              para solicitar atencion para perros y gatos.
            </p>
            <div class="hero-actions">
              <a class="btn btn-primary btn-lg" href="#solicitar-turno">Reservar ahora</a>
              <a class="btn btn-outline-dark btn-lg" href="#disponibles">Ver agenda</a>
            </div>
          </div>
          <div class="col-12 col-xl-5">
            <div class="hero-panel">
              <div class="hero-panel-label">Especialidades</div>
              <div class="chip-grid">
                {"".join(f'<span class="chip">{html.escape(item)}</span>' for item in SPECIALTIES)}
              </div>
              <div class="hero-panel-note">
                {len(available_slots())} turnos publicados ahora
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <main class="container pb-5">
      {build_alert(message, kind)}

      <section class="stats-row">
        <div class="stat-card">
          <span>Turnos disponibles</span>
          <strong>{len(available_slots())}</strong>
        </div>
        <div class="stat-card">
          <span>Solicitudes cargadas</span>
          <strong>{len(BOOKED_APPOINTMENTS)}</strong>
        </div>
        <div class="stat-card">
          <span>Atencion</span>
          <strong>Consultorio y virtual</strong>
        </div>
      </section>

      <section id="disponibles" class="section-block">
        <div class="section-heading">
          <div>
            <span class="section-kicker">Agenda publica</span>
            <h2>Turnos disponibles</h2>
            <p>Selecciona un horario y luego completa los datos del tutor para confirmar la solicitud.</p>
          </div>
        </div>
        <div class="row g-3">
          {build_slot_cards()}
        </div>
      </section>

      <section class="section-block">
        <div class="row g-4">
          <div class="col-12 col-lg-7">
            <div class="form-shell" id="solicitar-turno">
              <div class="section-heading mb-3">
                <div>
                  <span class="section-kicker">Solicitud</span>
                  <h2>Pedir turno</h2>
                  <p>Este mock registra solicitudes en memoria. Al reiniciar la app, la agenda vuelve al estado inicial.</p>
                </div>
              </div>
              <form method="post" action="/reservar" class="row g-3">
                <div class="col-12">
                  <label for="slot_id" class="form-label">Turno</label>
                  <select class="form-select" id="slot_id" name="slot_id" required>
                    {build_slot_options(form_data.get("slot_id", ""))}
                  </select>
                </div>
                <div class="col-12 col-md-6">
                  <label for="patient_name" class="form-label">Nombre del tutor</label>
                  <input class="form-control" id="patient_name" name="patient_name" required value="{html.escape(form_data.get("patient_name", ""))}">
                </div>
                <div class="col-12 col-md-6">
                  <label for="dni" class="form-label">Nombre de la mascota</label>
                  <input class="form-control" id="dni" name="dni" required value="{html.escape(form_data.get("dni", ""))}">
                </div>
                <div class="col-12 col-md-6">
                  <label for="email" class="form-label">Email</label>
                  <input type="email" class="form-control" id="email" name="email" required value="{html.escape(form_data.get("email", ""))}">
                </div>
                <div class="col-12 col-md-6">
                  <label for="phone" class="form-label">Telefono</label>
                  <input class="form-control" id="phone" name="phone" required value="{html.escape(form_data.get("phone", ""))}">
                </div>
                <div class="col-12">
                  <label for="notes" class="form-label">Motivo de la consulta</label>
                  <textarea class="form-control" id="notes" name="notes" rows="4" placeholder="Control, vacuna, picazon, dolor, seguimiento...">{html.escape(form_data.get("notes", ""))}</textarea>
                </div>
                <div class="col-12 d-flex gap-3 flex-wrap">
                  <button class="btn btn-primary btn-lg" type="submit">Confirmar solicitud</button>
                  <a class="btn btn-outline-secondary btn-lg" href="/">Limpiar</a>
                </div>
              </form>
            </div>
          </div>

          <div class="col-12 col-lg-5">
            <div class="side-panel">
              <span class="section-kicker">Actividad</span>
              <h2>Ultimas solicitudes</h2>
              <div class="request-list">
                {build_recent_requests()}
              </div>
            </div>
            <div class="side-panel mt-4">
              <span class="section-kicker">Como funciona</span>
              <div class="feature-list">
                <div><strong>1.</strong> El tutor elige un turno disponible.</div>
                <div><strong>2.</strong> Completa los datos de contacto y de la mascota.</div>
                <div><strong>3.</strong> El sistema confirma la solicitud y oculta ese horario.</div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </body>
</html>
"""
    return page.encode("utf-8")


class AppointmentHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/" or self.path.startswith("/?"):
            self._send_html(render_home())
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")

    def do_HEAD(self) -> None:
        if self.path == "/" or self.path.startswith("/?"):
            body = render_home()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")

    def do_POST(self) -> None:
        if self.path != "/reservar":
            self.send_error(HTTPStatus.NOT_FOUND, "Ruta no encontrada")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_data = self.rfile.read(content_length).decode("utf-8")
        parsed = {key: values[0].strip() for key, values in parse_qs(raw_data).items()}

        required_fields = ["slot_id", "patient_name", "dni", "email", "phone"]
        missing_fields = [field for field in required_fields if not parsed.get(field)]
        if missing_fields:
            self._send_html(
                render_home("Completa todos los campos obligatorios para solicitar el turno.", "danger", parsed),
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        slot = find_slot(parsed["slot_id"])
        if not slot:
            self._send_html(
                render_home("El turno seleccionado no existe.", "danger", parsed),
                status=HTTPStatus.BAD_REQUEST,
            )
            return

        if slot not in available_slots():
            self._send_html(
                render_home("Ese turno ya fue solicitado. Elige otro horario disponible.", "warning", parsed),
                status=HTTPStatus.CONFLICT,
            )
            return

        BOOKED_APPOINTMENTS.append(
            {
                "slot_id": parsed["slot_id"],
                "patient_name": parsed["patient_name"],
                "dni": parsed["dni"],
                "email": parsed["email"],
                "phone": parsed["phone"],
                "notes": parsed.get("notes", ""),
            }
        )
        success_message = (
            f"Solicitud registrada para {parsed['patient_name']} el {slot['date']} a las {slot['time']} "
            f"con {slot['professional']}."
        )
        self._send_html(render_home(success_message, "success"))

    def _send_html(self, body: bytes, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


STYLE_CSS = """
:root {
  --bg: #fff8ef;
  --surface: rgba(255, 255, 255, 0.82);
  --surface-strong: #ffffff;
  --line: rgba(88, 73, 42, 0.10);
  --text: #4b3f2f;
  --muted: #7a6e60;
  --primary: #f08c5a;
  --primary-dark: #d96b3b;
  --accent: #7cbf9e;
  --shadow: 0 22px 50px rgba(163, 120, 73, 0.12);
}

body {
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(240, 140, 90, 0.20), transparent 30%),
    radial-gradient(circle at top right, rgba(124, 191, 158, 0.22), transparent 24%),
    linear-gradient(180deg, #fffdf9 0%, var(--bg) 100%);
}

.app-nav {
  background: rgba(255, 253, 249, 0.9);
  backdrop-filter: blur(18px);
  border-bottom: 1px solid var(--line);
}

.navbar-brand {
  font-weight: 800;
  color: var(--primary);
}

.hero {
  padding: 4rem 0 2rem;
}

.eyebrow,
.section-kicker,
.hero-panel-label,
.slot-badge {
  display: inline-block;
  font-size: 0.76rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-weight: 800;
  color: var(--accent);
}

.hero h1,
.section-heading h2,
.side-panel h2 {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.05;
}

.hero h1 {
  font-size: clamp(2.8rem, 6vw, 5.3rem);
  max-width: 11ch;
  margin: 0.5rem 0 1rem;
}

.hero-copy,
.section-heading p,
.hero-panel-note,
.request-item span,
.feature-list div {
  color: var(--muted);
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 1.75rem;
}

.hero-panel,
.slot-card,
.form-shell,
.side-panel,
.stat-card,
.empty-state {
  background: var(--surface);
  border: 1px solid rgba(255, 255, 255, 0.55);
  border-radius: 1.5rem;
  box-shadow: var(--shadow);
}

.hero-panel,
.form-shell,
.side-panel {
  padding: 1.5rem;
}

.chip-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem;
  margin-top: 1rem;
}

.chip {
  background: rgba(124, 191, 158, 0.18);
  color: #466f5b;
  border-radius: 999px;
  padding: 0.55rem 0.85rem;
  font-weight: 600;
}

.hero-panel-note {
  margin-top: 1rem;
  font-weight: 700;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  margin-bottom: 3rem;
}

.stat-card {
  padding: 1.15rem 1.25rem;
}

.stat-card span {
  display: block;
  font-size: 0.9rem;
  color: var(--muted);
}

.stat-card strong {
  display: block;
  font-size: 1.6rem;
  margin-top: 0.2rem;
}

.section-block {
  margin-bottom: 3rem;
}

.section-heading {
  margin-bottom: 1.2rem;
}

.section-heading h2,
.side-panel h2 {
  margin: 0.4rem 0 0.5rem;
  font-size: clamp(1.9rem, 3vw, 2.7rem);
}

.slot-card {
  padding: 1.25rem;
}

.slot-card h3 {
  margin: 0.7rem 0 1rem;
  font-size: 1.2rem;
}

.slot-list {
  list-style: none;
  padding: 0;
  margin: 0 0 1.25rem;
}

.slot-list li {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: 0.6rem;
}

.request-list {
  display: grid;
  gap: 0.85rem;
}

.request-item {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid var(--line);
}

.request-item strong,
.request-item span {
  display: block;
}

.request-time {
  white-space: nowrap;
  font-weight: 700;
  color: var(--primary-dark);
}

.feature-list {
  display: grid;
  gap: 0.85rem;
}

.empty-state {
  padding: 1.25rem;
  color: var(--muted);
}

.empty-state.compact {
  box-shadow: none;
  border-style: dashed;
}

.btn-primary {
  --bs-btn-bg: var(--primary);
  --bs-btn-border-color: var(--primary);
  --bs-btn-hover-bg: var(--primary-dark);
  --bs-btn-hover-border-color: var(--primary-dark);
}

.form-control,
.form-select {
  border-radius: 0.9rem;
  padding: 0.8rem 0.95rem;
}

@media (max-width: 991.98px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .request-item {
    flex-direction: column;
  }
}
"""


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), AppointmentHandler)
    print(f"Servidor disponible en http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
