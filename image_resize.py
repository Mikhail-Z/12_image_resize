import argparse
from PIL import Image
import os


def arg_parse():
    parser = argparse.ArgumentParser("Image resizer", description="Sript resizes image given as the first argument")
    parser.add_argument("--input_file", type=str)
    parser.add_argument("--width", metavar="w", nargs="?", type=int)
    parser.add_argument("--height", metavar="h", nargs="?", type=int)
    parser.add_argument("--scale", metavar="s", nargs="?", type=float)
    parser.add_argument("--output_file", nargs="?", type=str)
    args = parser.parse_args()
    return args


def args_check(args):
    if file_args_check(args) and size_args_check(args):
        return True
    else:
        return False


def file_args_check(args):
    if args.input_file:
        if args.output_file and check_io_files_existence(args.input, args.output_file) or \
                not args.output_file and os.path.exists(args.input_file):
            return True
    return False


def size_args_check(args):
    if (args.width and args.height) and not args.scale or args.scale and not (args.width or args.height):
        return True
    else:
        return False


def resize_image(input_file, output_file, width, height, scale):
    path_to_original = input_file
    im = Image.open(path_to_original)
    if args.scale:
        new_width, new_height = get_new_width_and_height(im.size[0], im.size[1], scale)
    else:
        new_width, new_height = width, height
    if round(im.size[0]/im.size[1], 2) != round(new_width/new_height, 2):
        print("Note, the proportion of width and height will be changed!")

    if not output_file:
        path_to_result = get_path_to_result(path_to_original, new_width, new_height)
    else:
        path_to_result = args.output_file

    output_image = im.resize((new_width, new_height))
    output_image.save(path_to_result)


def check_io_files_existence(path_to_original, path_to_result):
    if not(os.path.exists(path_to_original)) or not os.path.exists(path_to_result):
        return False
    return True


def get_new_width_and_height(old_width, old_height, scale):
    new_width = int(old_width * scale)
    new_height = int(old_height * scale)
    return new_width, new_height


def get_path_to_result(path_to_original, new_width, new_height):
    file_name, extension = os.path.splitext(path_to_original)
    path_to_result = "{filename}{0}{width}{1}{height}{ext}".format("_", "x", filename=file_name, width=new_width,
                                                                   height=new_height, ext=extension)
    return path_to_result


if __name__ == '__main__':
    args = arg_parse()
    if args_check(args):
        resize_image(args.input_file, args.output_file, args.width, args.height, args.scale)
        print("Done!")
    else:
        print("Something went wrong."
              "Check input/output file existence and if you entered both width and height or scale!")