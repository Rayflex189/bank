import os

template_dir = r"c:\Users\suobo\.gemini\antigravity-ide\scratch\bank\wealthbridge\bank_app\templates\bank_app"

for filename in os.listdir(template_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(template_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "theme-override.css" not in content:
            if "</head>" in content:
                new_content = content.replace("</head>", "    <link rel=\"stylesheet\" href=\"{% static 'css/theme-override.css' %}\">\n</head>")
            elif "</HEAD>" in content:
                new_content = content.replace("</HEAD>", "    <link rel=\"stylesheet\" href=\"{% static 'css/theme-override.css' %}\">\n</HEAD>")
            elif "</style>" in content:
                new_content = content.replace("</style>", "    </style>\n    <link rel=\"stylesheet\" href=\"{% static 'css/theme-override.css' %}\">")
            else:
                print(f"No head/style tag found in {filename}")
                continue
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Updated {filename}")
        else:
            print(f"Already linked in {filename}")
