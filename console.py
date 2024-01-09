#!/usr/bin/python3
"""This is a module that defines the class `HBNBCommand`"""
import cmd
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex
import models

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class HBNBCommand(cmd.Cmd):
    """This command defines the entry point of the command interpreter"""
    prompt = "(hbnb) "

    def do_quit(self, line):
        """This command exits the program
        """
        return True

    def do_EOF(self, line):
        """This command exits the program with EOF
        """
        return True

    def emptyline(self):
        """This command defines what happens when the `Enter` key is pressed
        """
        pass

    def do_create(self, args):
        """This command creates a new instance of BaseModel,
          Command syntax: create <Class name> <param 1> <param 2> <param 3>
          saves it (to the JSON file)
           and prints the id
        """
        from models import storage
        from models.base_model import BaseModel
        args_list = args.split()
        class_name = args_list[0]
        if len(args_list) < 2:
            print("** class name missing **")
            return
        if class_name not in classes:
            print("** class doesn't exist **")
            return

        try:
            instance = eval(class_name)()
        except Exception as e:
            print(f"Error creating instance: {e}")
            return
        last_processed_value = None
        key = ""
        value = ""
        params = ' '.join(args_list[1:])
        param_list = [param.strip() for param in params.split()]
        for param in param_list:
            key_value = param.split('=')
            if len(key_value) == 2:
                key, raw_value = key_value[0], key_value[1]
                if raw_value.startswith('"') and raw_value.endswith('"'):
                    value = raw_value[1:-1].replace('_', ' ')
                elif '.' in raw_value:
                    try:
                        value = float(raw_value)
                    except ValueError:
                        continue
                else:
                    try:
                        value = int(raw_value)
                    except ValueError:
                        continue
                setattr(instance, key, value)
                last_processed_value = value
        instance.save()
        print(instance.id)

    def do_show(self, args):
        """this command prints the string representation of an instance
           based on the
           class name and id
        """
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            instance_key = f'{args[0]}.{args[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[instance_key])

    def do_destroy(self, args):
        """This command deletes an instance based on the class name and id
        """
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            instance_key = f'{args[0]}.{args[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                del(storage.all()[instance_key])
                storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based or
            not on the class name
        """
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            obj_dict = models.storage.all()
        if len(args) == 1:
            class_name = args[0]
            if class_name in classes:
                obj_dict = models.storage.all(classes[class_name])
            else:
                print("** class doesn't exist **")
                return False
        for key in obj_dict:
            obj_list.append(str(obj_dict[key]))
        print("[", end="")
        print(", ".join(obj_list), end="")
        print("]")

    def do_update(self, args):
        """Updates an instance based on the class name and id
        by adding or updating attribute
        """
        args = args.split()
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        else:
            instance_key = f'{args[0]}.{args[1]}'
            if instance_key not in storage.all():
                print("** no instance found **")
            else:
                obj = storage.all()[instance_key]
                try:
                    setattr(obj, args[2], eval(args[3]))
                except NameError:
                    setattr(obj, args[2], args[3])
                obj.save()

    def default(self, arg):
        "Defines any other command"
        args = arg.split('.')
        if args[0] in classes:
            if args[1] == "all()":
                self.do_all(args[0])
            elif args[1] == "count()":
                count = 0
                for key in storage.all():
                    if key.startswith(args[0]):
                        count += 1
                print(count)
            elif args[1].startswith("show"):
                uuid = eval(args[1].strip("show()"))
                self.do_show(f"{args[0]} {uuid}")
            elif args[1].startswith("destroy"):
                uuid = eval(args[1].strip("destroy()"))
                self.do_destroy(f"{args[0]} {uuid}")
            elif args[1].startswith("update"):
                if args[1].endswith("})"):
                    entry = args[1].strip("update()").strip("}").split(", {")
                    uuid = eval(entry[0])
                    dictionary = eval('{' + entry[1] + '}')
                    for name, value in dictionary.items():
                        self.do_update(f"{args[0]} {uuid} {name} {value}")
                else:
                    entry = args[1].strip("update()").split(", ")
                    uuid = eval(entry[0])
                    name = eval(entry[1])
                    value = entry[2]
                    self.do_update(f"{args[0]} {uuid} {name} {value}")


if __name__ == '__main__':
    from models import storage
    HBNBCommand().cmdloop()
