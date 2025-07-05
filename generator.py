import re
import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkfont
from PIL import Image, ImageDraw, ImageFont, ImageTk

# --- CONFIG ---
TEMPLATE_PATH = "Templates/"
ICON_PATH = "Icons/"
RARITY_PATH = "Rarity/"
FONT_PATH = "Cafeteria-Bold.otf"
BACKGROUND_PATH = "Background.png"
TOKEN_PATTERN = re.compile(r"(:[a-zA-Z0-9+\-]+:)|(\*\*.*?\*\*)")
ICON_ID_PATTERN = re.compile(r"^([a-zA-Z]+)([0-9+\-]+)?$")
ICON_SIZE = 32

class ImageGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PvZ Heroes Card Generator")
        self.ui_font = tkfont.Font(family="Georgia", size=18)
        self.user_image_path = None

        # --- Load background image ---
        self.bg_image = Image.open(BACKGROUND_PATH)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        bg_label = tk.Label(root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # --- Main layout frames ---
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side="left", padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", padx=10, pady=10)

        # --- Dropdowns and input fields ---
        tk.Label(self.left_frame, text="Class:", font=self.ui_font).grid(row=0, column=0, sticky="w")
        self.family = tk.StringVar()
        tk.OptionMenu(self.left_frame, self.family, "Guardian", "Kabloom", "MegaGrow", "Smarty", "Solar", "Beastly", "Brainy", "Crazy", "Hearty", "Sneaky").grid(row=0, column=1, sticky="w")
        self.family.set("Guardian")

        tk.Label(self.left_frame, text="Type:", font=self.ui_font).grid(row=0, column=2, sticky="w")
        self.cardtype = tk.StringVar()
        tk.OptionMenu(self.left_frame, self.cardtype, "Minion", "Trick", "Environment").grid(row=0, column=3, sticky="w")
        self.cardtype.set("Minion")

        tk.Label(self.left_frame, text="Rarity:", font=self.ui_font).grid(row=1, column=0, sticky="w")
        self.rarity = tk.StringVar()
        tk.OptionMenu(self.left_frame, self.rarity, "Token", "Common", "Uncommon", "Rare", "SuperRare", "Legendary", "Event").grid(row=1, column=1, sticky="w")
        self.rarity.set("Common")

        tk.Label(self.left_frame, text="Set:", font=self.ui_font).grid(row=1, column=2, sticky="w")
        self.set = tk.Entry(self.left_frame, width=12)
        self.set.grid(row=1, column=3, sticky="w")

        tk.Label(self.left_frame, text="Name:", font=self.ui_font).grid(row=2, column=0, sticky="w")
        self.name = tk.Entry(self.left_frame, width=12)
        self.name.grid(row=2, column=1, sticky="w")

        tk.Label(self.left_frame, text="Tribes:", font=self.ui_font).grid(row=2, column=2, sticky="w")
        self.tribes = tk.Entry(self.left_frame, width=12)
        self.tribes.grid(row=2, column=3, sticky="w")

        tk.Label(self.left_frame, text="Cost:", font=self.ui_font).grid(row=3, column=0, sticky="w")
        self.cost = tk.Entry(self.left_frame, width=8)
        self.cost.grid(row=3, column=1, sticky="w")

        tk.Label(self.left_frame, text="Attack:", font=self.ui_font).grid(row=4, column=0, sticky="w")
        self.atk = tk.Entry(self.left_frame, width=8)
        self.atk.grid(row=4, column=1, sticky="w")

        tk.Label(self.left_frame, text="Health:", font=self.ui_font).grid(row=4, column=2, sticky="w")
        self.hp = tk.Entry(self.left_frame, width=8)
        self.hp.grid(row=4, column=3, sticky="w")

        tk.Label(self.left_frame, text="Icon:", font=self.ui_font).grid(row=5, column=0, sticky="w")
        self.atkicon = tk.StringVar()
        tk.OptionMenu(self.left_frame, self.atkicon, "Normal", "AntiHero", "Bullseye", "Deadly", "DoubleStrike", "Frenzy", "Overshoot", "Strikethrough", "Multi").grid(row=5, column=1, sticky="w")
        self.atkicon.set("Normal")

        tk.Label(self.left_frame, text="Icon:", font=self.ui_font).grid(row=5, column=2, sticky="w")
        self.hpicon = tk.StringVar()
        tk.OptionMenu(self.left_frame, self.hpicon, "Normal", "Armored", "Shielded", "StrengthHeart", "Untrickable", "Multi").grid(row=5, column=3, sticky="w")
        self.hpicon.set("Normal")

        tk.Label(self.left_frame, text="Ability:", font=self.ui_font).grid(row=6, column=0, sticky="nw")
        self.ability = tk.Text(self.left_frame, width=50, height=3)
        self.ability.grid(row=6, column=1, columnspan=5, sticky="w")

        tk.Label(self.left_frame, text="Flavor:", font=self.ui_font).grid(row=7, column=0, sticky="nw")
        self.flavor = tk.Text(self.left_frame, width=50, height=3)
        self.flavor.grid(row=7, column=1, columnspan=5, sticky="w")

        # --- Buttons and sliders ---
        tk.Button(self.left_frame, text="Upload Image", command=self.upload_user_image, font=self.ui_font).grid(row=8, column=0, columnspan=6, pady=(5, 10), sticky="we")

        tk.Label(self.left_frame, text="Scale:", font=self.ui_font).grid(row=9, column=0, sticky="w")
        self.scale_slider = tk.Scale(self.left_frame, from_=0.5, to=2, orient="horizontal", resolution=0.01, command=self.on_slider_move)
        self.scale_slider.set(1)
        self.scale_slider.grid(row=9, column=1, columnspan=5, sticky="we")

        tk.Label(self.left_frame, text="X:", font=self.ui_font).grid(row=10, column=0, sticky="w")
        self.x_slider = tk.Scale(self.left_frame, from_=-100, to=100, orient="horizontal", resolution=1, command=self.on_slider_move)
        self.x_slider.set(0)
        self.x_slider.grid(row=10, column=1, columnspan=5, sticky="we")

        tk.Label(self.left_frame, text="Y:", font=self.ui_font).grid(row=11, column=0, sticky="w")
        self.y_slider = tk.Scale(self.left_frame, from_=-100, to=100, orient="horizontal", resolution=1, command=self.on_slider_move)
        self.y_slider.set(0)
        self.y_slider.grid(row=11, column=1, columnspan=5, sticky="we")

        tk.Button(self.left_frame, text="Preview Image", command=self.preview_image, font=self.ui_font).grid(row=12, column=0, columnspan=6, pady=(10, 2), sticky="we")
        tk.Button(self.left_frame, text="Save Image", command=self.save_image, font=self.ui_font).grid(row=13, column=0, columnspan=6, sticky="we")

        # Right: Image preview
        self.canvas = tk.Label(self.right_frame)
        self.canvas.pack()

        self.generated_image = None
        self.preview_image()

    def upload_user_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.webp;*.bmp")],
            title="Select card image"
        )
        if filepath:
            self.user_image_path = filepath
            self.preview_image()

    def on_slider_move(self, _):
        return
        self.preview_image()

    def render_line_with_outline(self, draw, text, x, y, font, fill="white", outline_color="black", stroke_width=1, thin=False):
        dx_arr = [-stroke_width, 0]
        dy_arr = [-stroke_width, 0]

        if not thin:
            dx_arr.append(stroke_width)
            dy_arr.append(stroke_width)

        for dx in dx_arr:
            for dy in dy_arr:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

        draw.text((x, y), text, font=font, fill=fill)

    def render_line_with_icons(self, base, line, y, draw, font, fill="white"):
        segments = TOKEN_PATTERN.split(line)
        content = []

        total_width = 0
        max_height = 0

        for segment in segments:
            if not segment:
                continue
            if segment.startswith(":") and segment.endswith(":"):
                token = segment[1:-1]
                match = ICON_ID_PATTERN.fullmatch(token)

                if match:
                    base_name, suffix = match.groups()
                    icon_path = ICON_PATH + base_name + ".png"

                    try:
                        icon = Image.open(icon_path).convert("RGBA")
                        scale = ICON_SIZE / icon.height
                        icon = icon.resize((int(icon.width * scale), ICON_SIZE), Image.LANCZOS)

                        if suffix:
                            # Draw suffix text on top
                            overlay = Image.new("RGBA", icon.size, (0, 0, 0, 0))
                            overlay_draw = ImageDraw.Draw(overlay)
                            font_suffix = ImageFont.truetype(FONT_PATH, 24)

                            w_text = draw.textlength(suffix, font=font_suffix)
                            h_text = font_suffix.getbbox(suffix)[3]
                            tx = (icon.width - w_text) // 2
                            ty = (icon.height - h_text) // 2 - 2
                            self.render_line_with_outline(overlay_draw, suffix, tx, ty, font_suffix)

                            icon = Image.alpha_composite(icon, overlay)

                        content.append(("icon", icon))
                        total_width += icon.width
                        max_height = max(max_height, icon.height)
                    except FileNotFoundError:
                        content.append(("text", segment))
                        total_width += draw.textlength(segment, font=font)
                        max_height = max(max_height, font.getbbox(segment)[3])
            elif segment.startswith("**") and segment.endswith("**"):
                bold_text = segment[2:-2]
                content.append(("bold", bold_text))
                total_width += draw.textlength(bold_text, font=font)
                max_height = max(max_height, font.getbbox(bold_text)[3])
            else:
                content.append(("text", segment))
                total_width += draw.textlength(segment, font=font)
                max_height = max(max_height, font.getbbox(segment)[3])

        # Center the line
        w_bg = base.width
        x = (w_bg - total_width) // 2

        for typ, obj in content:
            if typ == "text":
                draw.text((int(x), y), obj, font=font, fill=fill)
                x += draw.textlength(obj, font=font)
            elif typ == "bold":
                self.render_line_with_outline(draw, obj, int(x), y, font, fill=fill, outline_color=fill, thin=True)
                x += draw.textlength(obj, font=font)
            elif typ == "icon":
                base.paste(obj, (int(x), y), mask=obj)
                x += obj.width

        return int(max_height)
    
    def generate_class_template(self, base, selected_family):
        w_bg = base.width

        body = Image.open(TEMPLATE_PATH + selected_family + ".png").convert("RGBA")
        top = Image.open(TEMPLATE_PATH + selected_family + "2.png").convert("RGBA")
        class_icon = Image.open(ICON_PATH + selected_family + ".png").convert("RGBA")

        scale_body, scale_top, scale_class = 0.275, 0.16, 0.55
        w_body, h_body = body.size
        w_top, h_top = top.size
        w_class, h_class = class_icon.size
        w_body, h_body = int(w_body * scale_body), int(h_body * scale_body)
        w_top, h_top = int(w_top * scale_top), int(h_top * scale_top)
        w_class, h_class = int(w_class * scale_class), int(h_class * scale_class)

        body_resized = body.resize((w_body, h_body), Image.LANCZOS)
        top_resized = top.resize((w_top, h_top), Image.LANCZOS)
        class_resized = class_icon.resize((w_class, h_class), Image.LANCZOS)

        x_body, y_body = (w_bg - w_body) // 2, 300
        x_top, y_top = (w_bg - w_top) // 2, 130
        x_class, y_class = 485, 275

        base.paste(body_resized, (x_body, y_body), mask=body_resized)
        base.paste(top_resized, (x_top, y_top), mask=top_resized)
        base.paste(class_resized, (x_class, y_class), mask=class_resized)

    def generate_rarity_banner(self, base, draw, selected_rarity, set_name):
        w_bg = base.width

        rarity_banner = Image.open(RARITY_PATH + selected_rarity + ".png").convert("RGBA")

        scale_rarity = 1.1
        w_rarity, h_rarity = rarity_banner.size
        w_rarity, h_rarity = int(w_rarity * scale_rarity), int(h_rarity * scale_rarity)

        rarity_resized = rarity_banner.resize((w_rarity, h_rarity), Image.LANCZOS)
        x_rarity, y_rarity = (w_bg - w_rarity) // 2, 620
        base.paste(rarity_resized, (x_rarity, y_rarity), mask=rarity_resized)

        font_rarity = ImageFont.truetype(FONT_PATH, 50)
        rarity_text = set_name
        rarity_color = "#ffffff"
        if selected_rarity == "Event" or selected_rarity == "Token":
            rarity_text = selected_rarity.upper()
        elif selected_rarity == "SuperRare":
            rarity_text += " - SUPER-RARE"
        else:
            rarity_text += " - " + selected_rarity.upper()

        w_rarity_text = draw.textlength(rarity_text, font=font_rarity)
        x_rarity_text, y_rarity_text = x_rarity + (w_rarity - w_rarity_text) // 2, 687

        if (selected_rarity == "Common" or selected_rarity == "Token" or selected_rarity == "Uncommon"):
            y_rarity_text += 5
        elif selected_rarity == "Rare":
            y_rarity_text += 5
            rarity_color = "#fced8f"
        elif selected_rarity == "SuperRare":
            y_rarity_text += 2
            rarity_color = "#b2dcfc"

        self.render_line_with_outline(draw, rarity_text, x_rarity_text, y_rarity_text, font_rarity, fill=rarity_color)
    
    def generate_card_image(self, base, scale_adjust, x_adjust, y_adjust):
        user_img = Image.open(self.user_image_path).convert("RGBA")
        w_bg = base.width

        card_image_target_width = int(250 * scale_adjust)
        scale = card_image_target_width / user_img.width
        card_image_new_height = int(user_img.height * scale)

        user_img = user_img.resize((card_image_target_width, card_image_new_height), Image.LANCZOS)

        x_card_image, y_card_image = (w_bg - user_img.width) // 2 + x_adjust, 100 + y_adjust
        base.paste(user_img, (x_card_image, y_card_image), mask=user_img)

    def generate_card_name(self, base, draw, card_name):
        w_bg = base.width

        font_name = ImageFont.truetype(FONT_PATH, 60)
        w_name = draw.textlength(card_name, font=font_name)
        x_name, y_name = (w_bg - w_name) // 2, 380

        self.render_line_with_outline(draw, card_name, x_name, y_name, font_name)

    def generate_tribes(self, base, draw, tribes, selected_type, faction):
        w_bg = base.width

        font_tribes = ImageFont.truetype(FONT_PATH, 30)
        tribes_text = tribes
        if selected_type == "Minion":
            tribes_text += " " + faction[:-1]
        else:
            tribes_text += " " + selected_type

        tribes_text = "- " + tribes_text + " -"

        w_tribes = draw.textlength(tribes_text, font=font_tribes)
        x_tribes, y_tribes = (w_bg - w_tribes) // 2, 450
        draw.text((x_tribes, y_tribes), tribes_text, font=font_tribes, fill="#9c9c9c")

    def generate_stats(self, base, draw, cost, attack, health, atktype, hptype, selected_type, faction):
        w_bg = base.width

        cost_icon = Image.open(ICON_PATH + ("Sun" if faction == "Plants" else "Brain") + ".png").convert("RGBA")
        atk_icon = Image.open(ICON_PATH + ("Strength" if atktype == "Normal" else atktype) + ".png").convert("RGBA")
        hp_icon = Image.open(ICON_PATH + ("Health" if hptype == "Normal" else hptype) + ".png").convert("RGBA")

        scale_icon = 1.3
        w_icon, h_icon = cost_icon.size
        w_icon, h_icon = int(w_icon * scale_icon), int(h_icon * scale_icon)

        cost_resized = cost_icon.resize((w_icon, h_icon), Image.LANCZOS)
        atk_resized = atk_icon.resize((w_icon, h_icon), Image.LANCZOS)
        hp_resized = hp_icon.resize((w_icon, h_icon), Image.LANCZOS)

        if atktype == "Overshoot":
            atk_resized = atk_icon.resize((int(w_icon * 1.4), int(h_icon * 1.4)), Image.LANCZOS)

        x_cost, y_cost = 400, 130
        x_atk, y_atk = (w_bg - w_icon) // 2 - 35, 300
        x_hp, y_hp = (w_bg - w_icon) // 2 + 35, 300

        font_icon = ImageFont.truetype(FONT_PATH, 55)
        w_cost = draw.textlength(cost, font=font_icon)
        w_atk = draw.textlength(attack, font=font_icon)
        w_hp = draw.textlength(health, font=font_icon)
        x_cost_text, y_cost_text = x_cost + (w_icon - w_cost) // 2, y_cost + 10
        x_atk_text, y_atk_text = x_atk + (w_icon - w_atk) // 2, y_atk + 10
        x_hp_text, y_hp_text = x_hp + (w_icon - w_hp) // 2, y_hp + 10

        base.paste(cost_resized, (x_cost, y_cost), mask=cost_resized)
        draw.text((x_cost_text, y_cost_text), cost, font=font_icon, fill="black")

        if selected_type == "Minion":
            base.paste(hp_resized, (x_hp, y_hp), mask=hp_resized)
            self.render_line_with_outline(draw, health, x_hp_text, y_hp_text, font_icon)

            if attack != "0":
                if atktype == "Overshoot":
                    base.paste(atk_resized, (x_atk - 22, y_atk - 20), mask=atk_resized)
                else:
                    base.paste(atk_resized, (x_atk, y_atk), mask=atk_resized)

                self.render_line_with_outline(draw, attack, x_atk_text, y_atk_text, font_icon)

    def generate_ability_text(self, base, draw, ability_text):
        w_bg = base.width
        font_ability = ImageFont.truetype(FONT_PATH, 30)
        ability_lines = ability_text.splitlines()
        y_ability = 490
        line_spacing = 10

        for line in ability_lines:
            line_height = self.render_line_with_icons(base, line, y_ability, draw, font_ability)
            y_ability += line_height + line_spacing

    def generate_flavor_text(self, base, draw, flavor_text):
        w_bg = base.width

        font_flavor = ImageFont.truetype(FONT_PATH, 30)
        flavor_lines = flavor_text.splitlines()
        y_flavor = 800
        line_spacing = 10

        for line in flavor_lines:
            w_line = draw.textlength(line, font=font_flavor)
            x_line = (w_bg - w_line) // 2

            self.render_line_with_outline(draw, line, x_line, y_flavor, font_flavor)

            bbox = font_flavor.getbbox(line)
            h_line = bbox[3] - bbox[1]
            y_flavor += h_line + line_spacing

    def generate_image(self):
        # Gather input data
        selected_family = self.family.get()
        selected_type = self.cardtype.get()
        selected_rarity = self.rarity.get()
        set_name = self.set.get().strip()
        card_name = self.name.get().strip()
        tribes = self.tribes.get().strip()
        cost = self.cost.get().strip()
        attack = self.atk.get().strip()
        health = self.hp.get().strip()
        atktype = self.atkicon.get()
        hptype = self.hpicon.get()
        ability_text = self.ability.get("1.0", "end-1c")
        flavor_text = self.flavor.get("1.0", "end-1c")
        scale_adjust = self.scale_slider.get()
        x_adjust = self.x_slider.get()
        y_adjust = self.y_slider.get()

        faction = "Plants" if selected_family in ["Guardian", "Kabloom", "MegaGrow", "Smarty", "Solar"] else "Zombies"

        # Choose plant/zombie background based on class
        card_bg = TEMPLATE_PATH + faction + ".png"
        base = Image.open(card_bg).convert("RGBA")
        draw = ImageDraw.Draw(base)

        # Generate template from class
        self.generate_class_template(base, selected_family)

        # Display rarity banner
        self.generate_rarity_banner(base, draw, selected_rarity, set_name)

        # Display card image
        if self.user_image_path:
            self.generate_card_image(base, scale_adjust, x_adjust, y_adjust)

        # Display card name
        self.generate_card_name(base, draw, card_name)

        # Display tribes
        self.generate_tribes(base, draw, tribes, selected_type, faction)

        # Display stats
        self.generate_stats(base, draw, cost, attack, health, atktype, hptype, selected_type, faction)

        # Display ability text
        self.generate_ability_text(base, draw, ability_text)

        # Display flavor text
        self.generate_flavor_text(base, draw, flavor_text)

        return base

    def preview_image(self):
        img = self.generate_image()
        self.generated_image = img

        img_resized = img.resize((img.width // 2, img.height // 2))
        img_tk = ImageTk.PhotoImage(img_resized)
        self.canvas.configure(image=img_tk)
        self.canvas.image = img_tk

    def save_image(self):
        if self.generated_image:
            filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                    filetypes=[("PNG files", "*.png")])
            if filepath:
                self.generated_image.save(filepath)
        else:
            tk.messagebox.showinfo("No image", "Please preview an image first.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageGeneratorApp(root)
    root.mainloop()
