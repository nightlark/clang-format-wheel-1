import filecmp
import os
import pytest
import subprocess
import tempfile


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    subprocess.run("git init", shell=True)
    return tmp_path


@pytest.mark.parametrize("testcase", [("helloworld.cc", "helloworld_format.cc")])
def test_clang_format(testcase):
    # Get full paths to the test data
    test_input, test_output = testcase
    test_input = os.path.join(os.path.dirname(__file__), test_input)
    test_output = os.path.join(os.path.dirname(__file__), test_output)

    with tempfile.TemporaryDirectory() as tmp:
        outname = os.path.join(tmp, "formatted")
        with open(outname, "w") as out:
            subprocess.run(["clang-format", test_input], stdout=out, check=True)

        # Check that the content is equal
        assert filecmp.cmp(outname, test_output)


def test_git_clang_format(repo):
    # Test whether the git-clang-format tool is properly executable
    # on an empty git repository.

    # Create a commit with an empty file
    open(repo / "test", "w").close()
    subprocess.run("git add test", shell=True)
    subprocess.run("git commit -m initial", shell=True)

    # Check that the clang-format tool runs on the test repo
    subprocess.run("git clang-format", shell=True)
