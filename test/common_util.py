import os

sample_directory=os.path.join("test","samples")
expected_suffix='_expected'
valid_folder='valid'

def get_files_ending_with(folder, ending):
    return [os.path.join(folder,f) for f in os.listdir(folder)
                  if os.path.isfile(os.path.join(folder, f))
                  and f.endswith(ending)]


def get_sample_files_and_expected(root_folder, base_folder_name):
    sample_folder = os.path.join(root_folder, base_folder_name)
    expected_folder = os.path.join(root_folder, base_folder_name+expected_suffix)
    list_samples = get_files_ending_with(sample_folder, ".wrf")
    list_expected = get_files_ending_with(expected_folder, ".wrf.json")
    return list_samples, list_expected
