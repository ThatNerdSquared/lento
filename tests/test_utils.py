from lento import utils


def test_remove_dupes_blanks_and_whitespace():
    test_list = ["llamas   ", "are", "cool", "", "cool", "llamas", ""]
    new_list = utils.remove_dupes_blanks_and_whitespace(test_list)

    assert new_list == ["llamas", "are", "cool"]
