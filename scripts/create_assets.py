import os
from PIL import Image, ImageDraw

# Define the path to the assets folder
ASSETS_DIR = os.path.join("..", "app", "ui", "assets")


def generate_ui_images():
    try:
        # --- Create Unchecked Image ---
        img_unchecked = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_unchecked)
        draw.rounded_rectangle((0, 0, 23, 23), radius=5, outline="#565b5e", width=3)
        img_unchecked.save(os.path.join(ASSETS_DIR, "checkbox_unchecked.png"))
        print("Created checkbox_unchecked.png")

        # --- Create Checked Image ---
        img_checked = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_checked)
        draw.rounded_rectangle((0, 0, 23, 23), radius=5, fill="#3a7ebf")
        draw.line([(6, 12), (10, 16), (18, 8)], fill="white", width=3, joint="round")
        img_checked.save(os.path.join(ASSETS_DIR, "checkbox_checked.png"))
        print("Created checkbox_checked.png")

        # --- Create Indeterminate (Tri-State) Image ---
        img_indeterminate = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_indeterminate)
        draw.rounded_rectangle(
            (0, 0, 23, 23), radius=5, fill="#3a7ebf"
        )  # Filled blue box
        img_indeterminate.save(os.path.join(ASSETS_DIR, "checkbox_indeterminate.png"))
        print("Created checkbox_indeterminate.png")

        # --- Create Arrow Right (Collapsed) Image ---
        img_arrow_right = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_arrow_right)
        draw.polygon(
            [(6, 4), (16, 10), (6, 16)], fill="#3a7ebf"
        )  # White/light gray arrow
        img_arrow_right.save(os.path.join(ASSETS_DIR, "arrow_right.png"))
        print("Created arrow_right.png")

        # --- Create Arrow Down (Expanded) Image ---
        img_arrow_down = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img_arrow_down)
        draw.polygon([(4, 6), (10, 16), (16, 6)], fill="#3a7ebf")
        img_arrow_down.save(os.path.join(ASSETS_DIR, "arrow_down.png"))
        print("Created arrow_down.png")

    except Exception as e:
        print(f"An error occurred: {e}. Please ensure Pillow is installed.")


if __name__ == "__main__":
    os.makedirs(ASSETS_DIR, exist_ok=True)
    generate_ui_images()
