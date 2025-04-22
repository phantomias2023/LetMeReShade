def read_shortcuts_file(self) -> list:
    games = []
    try:
        with open("./shortcuts.vdf", 'rb') as f:
            shortcuts = str(f.read()).split('\\x00\\x02')

        for line in shortcuts:
            if 'appid\\x00' not in line or "emulation" in line.lower():
                continue

            gamedata = line.split('\\x00')
            name = ''
            exe = ''
            path = ''

            for index in range(len(gamedata)):
                if '\\x01AppName' in gamedata[index]:
                    name = gamedata[index+1].replace('\\', '')
                    continue
                elif gamedata[index] == '\\x01Exe':
                    exe = gamedata[index+1]
                    if "flatpak" in exe.lower() or "appimage" in exe.lower():
                        exe = None
                        break
                    continue
                elif gamedata[index] == '\\x01StartDir':
                    path = gamedata[index+1]
                    continue
                else:
                    continue

            if exe:
                games.append({"Name": name, "Exe": exe, "Path": path})

    except Exception as e:
        return []

    return games
