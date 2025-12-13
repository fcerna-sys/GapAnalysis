# Validador de Composición Atómica

## Reglas
- Átomos: no pueden contener bloques internos.
- Moléculas: solo pueden contener átomos.
- Organismos: pueden contener moléculas y átomos; no se permiten bloques ajenos ni `core/html`.
- HTML directo (`core/html`): prohibido en la composición.

## Funcionamiento
- Se ejecuta en `save_post` y guarda reporte en meta `img2html_composition_report`.
- Muestra aviso en el editor con el resultado.

## Extensión
- Ajusta reglas o severidad editando `php/composition-validator.php`.
- Futuros pasos: endpoint REST, bloqueo de publicación opcional, exclusiones por bloque.

