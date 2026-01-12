from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = True


if __name__ == '__main__':
    fetch_handler.fetch_series_info(FORCE_FETCH)
