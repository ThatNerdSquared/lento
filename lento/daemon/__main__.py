import proxy
from lento.daemon import get_proxy


def entry():
    with proxy.Proxy([
        "--port=0",
        "--plugins",
        "proxy.plugin.FilterByUpstreamHostPlugin",
        "--filtered-upstream-hosts",
        "slack.com,www.slack.com",
    ]) as lib_proxy:
        lento_proxy = get_proxy()
        result = lento_proxy.enable_system_proxy(lib_proxy.flags.port)
        print(result)
        proxy.sleep_loop()


if __name__ == '__main__':
    entry()
