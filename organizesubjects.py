import datetime
import os
import subprocess

class SubjectOrganizer(object):
    def __init__(self, skew):
        self._skew = datetime.timedelta(seconds=skew)
        self._subject_db = []

    def get_subject(self, input_file, file_date):
        db_index = self._search_for_existing_subject(file_date)
        if db_index is not None:
            subject = self._add_to_existing_subject(db_index, file_date)
        else:
            subject = self._get_subject_from_user(input_file)
            self._add_subject_to_db(file_date, subject)
        return subject

    def _add_subject_to_db(self, file_date, subject):
        self._subject_db.append([file_date, file_date, subject])

    def _search_for_existing_subject(self, file_date):
        if not self._subject_db:
            return None
        for index, (start_date, end_date, _) in enumerate(self._subject_db):
            if (file_date > (start_date - self._skew) and
                    file_date < (end_date + self._skew)):
                return index
        return None

    def _add_to_existing_subject(self, db_index, file_date):
        (start_date, end_date, subject) = self._subject_db[db_index]
        if file_date < start_date:
            self._subject_db[db_index][0] = file_date
        elif file_date > end_date:
            self._subject_db[db_index][1] = file_date
        return subject

    def _get_subject_from_user(self, input_file):
        with open(os.devnull, 'w') as dev_null:
            subprocess.call(['gwenview', input_file],
                            stdout=dev_null, stderr=dev_null)
        subject = None
        while not subject:
            subject = raw_input('Subject: ')
        return subject.replace(' ', '_')
