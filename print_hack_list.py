from common import data_handler, fetch_handler, file_helper, reference


FORCE_FETCH = False


if __name__ == '__main__':
    hack_names = fetch_handler.fetch_all_hack_names(FORCE_FETCH)
    print('\n'.join(hack_names))
