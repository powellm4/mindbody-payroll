import pandas
from cleaner_functions import *
from constants import uploads_folder_path


def run_data_cleaner(filename):
	print('Cleaning Mindbody Data...')
	create_folder(data_cleaner_output_folder)
	initial_read = pandas.read_html(uploads_folder_path + filename)
	master_list = remove_fluff_dfs_from_master_list(initial_read)
	initial_read = None
	instructor_df_groups = group_data_frames_by_instructor(master_list)

	for group in instructor_df_groups:
		instructor_name = get_instructor_name_for_group(master_list, group)
		move_header_row_to_top_of_data_frame(master_list, group)
		append_instructor_name_as_column(master_list, group, instructor_name)

	master_list = remove_totals_dfs_from_master_list(master_list)

	for index, df in enumerate(master_list):
		df = drop_nan_columns(df)
		df = format_column_headers(df)
		df = drop_unnecessary_columns(df)
		df = remove_quotes(df)
		df = format_client_name(df)
		df = sort_by_date_time(df)
		df = drop_duplicate_columns(df)
		master_list[index] = df
		write_df_to_csv(df)

	write_master_list_to_csv(master_list)

	print('Finished Data Cleaning')



