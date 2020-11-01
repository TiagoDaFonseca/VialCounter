from configparser import ConfigParser


def update_camera_settings(param1, param2, minR, maxR):
    conf = ConfigParser()

    conf["PROCESSING"] = {
        "param1": param1,
        "param2": param2,
        "min_radius": minR,
        "max_radius": maxR
    }

    # Write the above sections to the config.ini file
    with open('config.ini', 'w') as con:
        conf.write(con)

    import sys
    conf.write(sys.stdout)


def load_credentials():
    conf = ConfigParser()
    conf.read('config.ini')
    usr = str(conf.get('ADMIN', 'usr'))
    pss = str(conf.get('ADMIN', 'pass'))
    return usr, pss


def load_camera_settings():
    conf = ConfigParser()
    conf.read('config.ini')
    # Params
    p1 = int(conf.get('PROCESSING', 'param1'))
    p2 = int(conf.get('PROCESSING', 'param2'))
    minr = int(conf.get('PROCESSING', 'min_radius'))
    maxr = int(conf.get('PROCESSING', 'max_radius'))

    return p1, p2, minr, maxr


def save_session(last_trays, p1, p2, minR, maxR, ip, dir, db_name, col, usr, password):
    conf = ConfigParser()

    conf["LAST SESSION"] = {
        "last_trays": last_trays
    }
    conf["PROCESSING"] = {
        "param1": p1,
        "param2": p2,
        "min_radius": minR,
        "max_radius": maxR
    }
    conf["SERVER"] = {
        "ip": ip,
        "db": db_name,
        "col": col
    }
    conf["DIRECTORY"] = {
        "dir": dir
    }
    conf["ADMIN"] = {
        "usr": usr,
        "pass": password
    }

    # Write the above sections to the config.ini file
    with open('config.ini', 'w') as con:
        conf.write(con)


def load_last_session():
    conf = ConfigParser()
    conf.read('config.ini')
    trays = conf.get('LAST SESSION', 'last_trays')
    return trays


def load_directory():
    conf = ConfigParser()
    conf.read('config.ini')
    dir = conf.get('DIRECTORY', 'dir')
    return dir


def load_server_address():
    conf = ConfigParser()
    conf.read('config.ini')
    server = conf.get('SERVER', 'ip')
    db = conf.get('SERVER', 'db')
    col = conf.get('SERVER', 'col')

    return server, db, col


if __name__ == "__main__":

    # Get config parser object
    config_object = ConfigParser()

    # # Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
    # config_object["USERINFO"] = {
    #     "admin": "Tiago",
    #     "loginid": "tiagocunha",
    #     "password": "1234"
    # }
    #
    # config_object["SERVERCONFIG"] = {
    #     "host": "tutswiki.com",
    #     "port": "8080",
    #     "ipaddr": "8.8.8.8"
    # }
    #
    # config_object["PROCESSING"] = {
    #     "param1": 200,
    #     "param2": 25,
    #     "min_radius": 20,
    #     "max_radius": 40
    # }

    # Write the above sections to the config.ini file
    # with open('config.ini', 'w') as conf:
    #     config_object.write(conf)

    # READ parameters from config file
    #from configparser import ConfigParser
    config = ConfigParser()
    config.read('config.ini')
    # print(config.sections())
    # print(int(config.get('PROCESSING', 'param1')).__class__)
    config.set('PROCESSING', 'param1', '200')
    import sys
    config.write(sys.stdout)
