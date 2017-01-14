import argparse
from PIL import Image
import os


def arg_parse():
    parser = argparse.ArgumentParser("Image resizer", description="Sript resizes image given as the first argument")
    parser.add_argument("--input", type=str)
    parser.add_argument("--width", metavar="w", nargs="?", type=int)
    parser.add_argument("--height", metavar="h", nargs="?", type=int)
    parser.add_argument("--scale", metavar="s", nargs="?", type=float)
    parser.add_argument("--output", nargs="?", type=str)
    args = parser.parse_args()
    return args


def error_printer(error_id):
    if error_id == 1:
        print("No such file or directory")
    elif error_id == 2:
        print("You should enter both width and height or only scale.")


def warning_printer(warning_id):
    if warning_id == 1:
        print("Note, the proportion of width and height will be changed!")


def args_check(args):
    if (args.width and args.height) and not args.scale:
        return True
    elif args.scale and not (args.width and args.height):
        return True
    else:
        error_printer(2)
        return False


def resize_image(args):
    path_to_original = args.input
    im = Image.open(path_to_original)
    if args.scale:
        new_width, new_height = get_new_width_and_height(im.size[0], im.size[1], args.scale)
    else:
        new_width, new_height = args.width, args.height
    if im.size[0]/im.size[1] != new_width/new_height:
        warning_printer(1)

    if not args.output:
        path_to_result = get_path_to_result(path_to_original, new_width, new_height)
    else:
        path_to_result = args.output

    output_image = im.resize((new_width, new_height))
    output_image.save(path_to_result)


def check_file_existence(path_to_original, path_to_result):
    if not(os.path.exists(path_to_original)) or \
            (path_to_result and not os.path.exists(path_to_result)):
        error_printer(1)
        return False

    return True


def get_new_width_and_height(old_width, old_height, scale):
    new_width = int(old_width * scale)
    new_height = int(old_height * scale)
    return new_width, new_height


def get_path_to_result(path_to_original, new_width, new_height):
    file_name, extension = os.path.splitext(path_to_original)
    path_to_result = file_name + "_" + str(new_width) + "x" + str(new_height) + extension

    return path_to_result


if __name__ == '__main__':
    args = arg_parse()
    if args_check(args) and check_file_existence(args.input, args.output):
        resize_image(args)
        print("Done!")
