#!/usr/bin/env python3

"""
This module contains the entry point of the
command interpreter for HBNB console.
"""

from cmd import Cmd
from typing import Any, cast
import ast
import logging
import shlex

from models import storage
from models.basemodel import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


logging.basicConfig(
    level=logging.DEBUG,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    filename="console.log",
    force=True,
)

disable_logging: bool = False
if disable_logging:
    logging.disable(logging.CRITICAL)


class HBNBCommand(Cmd):
    """
    Defines the console or command interpreter.
    """

    Cmd.prompt = "(HBNB) "
    __classes: dict[str, Any] = {
    "BaseModel": BaseModel,
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}

    def preloop(self) -> None:
        print(
            """
Welcome to HBNB command line interpreter version 1.
Type anything and **Boom! Watch the magic unveil.
              """
        )
        logging.debug("Start Console.")

    def postloop(self) -> None:
        print("Bye, much love! See you again...")
        logging.debug("End Console.")

    def emptyline(self) -> bool:
        return False

    def do_quit(self, args: str) -> bool:
        return True

    def do_EOF(self, args: str) -> bool:
        print()
        return True
    
    def default(self, line: str) -> None:
        """
        Overides the default method of Cmd class to
        allow these commands:
            - <classname>.all()
            - <classname>.count()
            - <classname>.create()
            - <classname>.destroy()
            - <classname>.show()
            - <classname>.update()
        """
        methods: dict[str, Any] = {
            "all()": self.do_all,
            "count()": self.do_count,
            "create()": self.do_create,
            "destroy()": self.do_destroy,
            "show()": self.do_show,
            "update()": self.do_update,
        }
        parts = line.split(".")
        class_name = parts[0]
        method_and_id = parts[1]
        if len(parts) < 2:
            return super().default(line)
        
        fragments = method_and_id.partition("(")
        try:
            method_name = fragments[0] + fragments[1] + fragments[2][-1]
        except IndexError:
            return super().default(line)
        
        if method_name and method_name not in methods:
            return super().default(line)
        
        if method_name != "update()":
            args = class_name + " " + fragments[2][1:-2]
            methods[method_name](args)
            return
           
        id, data = ast.literal_eval(fragments[2][:-1])
        if isinstance(data, dict):
            data = cast(dict[str, Any], data)
            args = class_name + " " + id + " " + str(data)
        else:
            args = class_name + " " + fragments[2][:-1].replace(',', '')
        logging.debug(f"default_command_args: {args}")
        logging.debug(f"default_command_args: {method_name}")
        logging.debug(f"default_command_args: {type(args)}")
        logging.debug(f"default_command_args: {type(method_name)}")
        methods[method_name](args)
    

    def do_all(self, args: str):
        """
        Prints all string representation of all instances
        based or not on the class name.
        Ex: (HBNB) all BaseModel or $ all.
        """
        logging.debug(f"all_command_args: {args}")
        class_name = ""
        if args:
            class_name: str = args.split()[0].strip()
            if class_name not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return

        all_objects = storage.all()
        if class_name:
            class_objects = [str(obj) for k, obj in all_objects.items()
                         if class_name in k]
            print(class_objects)
        else:
            objects = [str(obj) for obj in all_objects.values()]
            print(objects)
    
    def do_count(self, args: str):
        """
        Returns the count of each object in the storage.
        """
        if not args:
            print("** class name missing **")
            return
        
        class_name: str = args.split()[0].strip()
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
    
        all_objects = storage.all()
        sum = 0
        for key in all_objects:
            if class_name in key:
                sum += 1
        print(sum)
            


    def do_create(self, arg: str):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id.
        Ex: (HBNB) create BaseModel
        """
        logging.debug(f"create_command_args: {arg}")
        if not arg:
            print("** class name missing **")
        
        class_name: str = arg.split()[0].strip()
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj = HBNBCommand.__classes[class_name]()
            obj.save()
            print(obj.id)


    def do_destroy(self, args: str):
        """
        Deletes an instance based on the class name and
        id (save the change into the JSON file).
        Ex: (HBNB) destroy BaseModel 1234-1234-1234.
        """
        if not args:
            print("** class name missing **")
            return

        parts = args.split()
        class_name = parts[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(parts) < 2:
            print("** instance id missing **")
            return

        obj_id = parts[1]
        all_objects = storage.all()
        key = f"{class_name}.{obj_id}"
        if key not in all_objects:
            print("** no instance found **")
            return

        del all_objects[key]
        storage.save()


    def do_show(self, args: str):
        """
        Prints the string representation of an
        instance based on the class name and id.
        Ex: (HBNB) show BaseModel 1234-1234-1234
        """
        if not args:
            print("** class name missing **")
            return

        parts = args.split()
        class_name = parts[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(parts) < 2:
            print("** instance id missing **")
            return

        obj_id = parts[1]
        all_objects = storage.all()
        key = f"{class_name}.{obj_id}"
        obj = all_objects.get(key)
        if not obj:
            print("** no instance found **")
            return
        print(obj)


    def do_update(self, args: str):
        """
        Updates an instance based on the class name and id by adding or
        updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com".
        Usage:
            - update <class name> <id> <attribute name> "<attribute value>"
            - update <class name> <id> <dictionary>
        """
        if not args:
            print("** class name missing **")
            return

        parts = args.partition(" ")
        class_name = parts[0]
        obj_id, _, raw_attr_data = parts[2].partition(" ")

        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if not obj_id:
            print("** instance id missing **")
            return

        all_objects = storage.all()
        key = f"{class_name}.{obj_id}"
        obj = all_objects.get(key)
        if not obj:
            print("** no instance found **")
            return
        
        try:
            parsed_data = ast.literal_eval(raw_attr_data)
        except Exception:
            parsed_data = None
        if isinstance(parsed_data, dict):
            attr_dict = cast(dict[str, Any], parsed_data)
            for key, value in attr_dict.items():
                setattr(obj, str(key), value)
            obj.save()
            return
        
        attr_parts = shlex.split(raw_attr_data)
        if not attr_parts:
            print(" ** attribute name missing **")
            return
        if len(attr_parts) == 1:
            print("** value missing **")
            return
        
        attr_name, attr_value = attr_parts[:2]
        if attr_value.isdigit():
            attr_value = int(attr_value)
        else:
            try:
                attr_value = float(attr_value)
            except ValueError:
                pass
        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
