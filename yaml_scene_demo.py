import yaml_scene as yaml
import ppm
import camera
import light
import color
import base

def main():
    print(f"[+] Loading scene from file 'resources/cover.yml'")
    try:
        result = yaml.load_scene(open("resources/cover.yml"))
    except Exception as ex:
        print(f"[-] Error: {ex}")
        return

    print(f"[*] Rendering canvas ...")
    canv = camera.render(result.camera, result.scene, progress_bar=True, desc='rendering')
    print(f"[*] Generating ppm data ...")
    ppm_data = ppm.canvas_to_ppm(canv)
    write_to_file(ppm_data, "yaml_scene.ppm")
    print('[+] SUCCESS')

def write_to_file(data, filename):
    print(f'[*] Writing ppm data to file "{filename}" ...')
    try:
        open(filename, 'w').write(data)
    except Exception as ex:
        print(f"[-] Error: {ex}")


if __name__ == '__main__':
    main()
