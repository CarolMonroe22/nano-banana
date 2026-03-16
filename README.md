# Nano Banana

Generate images using Google Generative AI via AI agents like Claude Code, Cursor, or Windsurf.

## Install

```bash
npx skills add CarolMonroe22/nano-banana
```

## Requirements

- `GOOGLE_AI_API_KEY` environment variable
- Python 3 with `google-generativeai` package

### First-time setup

1. Get your API key at https://aistudio.google.com/apikey (free)
2. Add to your shell:
   ```bash
   echo 'export GOOGLE_AI_API_KEY="your-key-here"' >> ~/.zshrc
   source ~/.zshrc
   ```

## Usage

Just ask your AI agent to generate an image:

- "Generate an illustration of a laptop with sparkles"
- "Create a product photo of a coffee mug"
- "Make a minimalist logo for a pet app"

The skill handles the rest: asks for style, size, model, builds the prompt, and generates.

## Supported Image Types

- Illustrations (watercolor, monochromatic, flat, line art)
- Product photos
- Lifestyle photos
- Logos
- UI mockups
- Patterns & textures

## Models & Cost

| Model | Cost/image | Best for |
|-------|-----------|----------|
| Nano Banana 2 (default) | ~$0.04 | Latest, fastest, good quality |
| Nano Banana Pro | ~$0.06 | Best quality, slower |
| Nano Banana (legacy) | ~$0.04 | Original model |

## Batch Generation

Generate multiple images in a consistent style:

- "Create 5 blog illustrations in the same watercolor style"
- "Generate an icon set of 8 items matching my brand colors"

The skill confirms total cost before starting.

## License

MIT

## Author

[Carol Monroe](https://carolmonroe.com) - AI builder and SupaSquad member
