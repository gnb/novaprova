#include "np/spiegel/spiegel.hxx"
#include "np/spiegel/dwarf/state.hxx"

using namespace std;
using namespace np::util;

int
main(int argc, char **argv)
{
    np::util::argv0 = argv[0];
    bool preorder = true;
    bool paths = false;
    const char *filename = 0;
    for (int i = 1 ; i < argc ; i++)
    {
	if (!strcmp(argv[i], "--preorder"))
	{
	    preorder = true;
	}
	else if (!strcmp(argv[i], "--recursive"))
	{
	    preorder = false;
	}
	else if (!strcmp(argv[i], "--paths"))
	{
	    paths = true;
	}
	else if (argv[i][0] == '-')
	{
usage:
	    fatal("Usage: testrunner info [--preorder|--recursive] [--paths] [executable]\n");
	}
	else
	{
	    if (filename)
		goto usage;
	    filename = argv[i];
	}
    }

    np::spiegel::dwarf::state_t state;
    if (filename)
    {
	if (!state.add_executable(filename))
	    return 1;
    }
    else
    {
	if (!state.add_self())
	    return 1;
    }
    state.dump_info(preorder, paths);

    return 0;
}

