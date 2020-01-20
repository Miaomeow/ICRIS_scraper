#!/usr/bin/env bash

today=$1

mongoexport --host localhost --db icris --collection companies --type=csv --out export/$today/basic_info.csv --fields \
basic_info.cr_no,\
basic_info.company_name_eng,\
basic_info.company_name_chi,\
basic_info.company_type,\
basic_info.date_of_incorporation,\
basic_info.status,\
basic_info.remarks,\
basic_info.winding_up_mode,\
basic_info.date_of_dissolution,\
basic_info.register_of_charges,\
basic_info.note

mongoexport --host localhost --db icris --collection companies --type=csv --out export/$today/name_history.csv --fields \
basic_info.cr_no,\
basic_info.company_name_eng,\
name_history.effective_date,\
name_history.eng,\
name_history.chi

mongoexport --host localhost --db icris --collection companies --type=csv --out export/$today/registered_office.csv --fields \
basic_info.cr_no,\
basic_info.company_name_eng,\
registered_office

mongoexport --host localhost --db icris --collection companies --type=csv --out export/$today/share_capital.csv --fields \
basic_info.cr_no,\
basic_info.company_name_eng,\
share_capital.issued,\
share_capital.paid_up






