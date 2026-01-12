from common import fetch_handler, file_helper, reference, src_helper, tool


FORCE_FETCH = True
USER_ID = 'qxkrpqm8'


if __name__ == '__main__':
    fetch_handler.fetch_run_list_for_user(USER_ID, FORCE_FETCH)
