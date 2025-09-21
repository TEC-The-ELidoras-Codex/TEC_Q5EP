# Pantheon / Skymap schema

Each entity represents a myth-science node that can be placed on a skymap and used as an archetype in chats.

Fields

- name: string (unique)
- type: string (e.g., deity, celestial, construct)
- ra_deg: number (Right Ascension in degrees, 0–360)
- dec_deg: number (Declination in degrees, -90–+90)
- tags: [string]
- domain: [string] (e.g., entropy, light, resonance)
- symbols: [string]
- palette: [hex-color]
- lore: string (short paragraph)
- traits: { light: string, shadow: string, guidance: string }
- prompts: { text: string, negative?: string }

Notes

- Coordinates are illustrative for narrative; adjust when aligning to real sky.
- Keep paragraphs concise; long-form essays live elsewhere and can be referenced with a path.
