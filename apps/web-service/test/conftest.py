def pytest_terminal_summary(terminalreporter, exitstatus, config):
    stats = terminalreporter.stats
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    skipped = len(stats.get("skipped", []))
    errors = len(stats.get("error", []))
    color = "red" if failed or errors else "green"
    terminalreporter.write_sep(
        "=",
        f"测试结果：通过 {passed} / 失败 {failed} / 跳过 {skipped} / 错误 {errors}",
        **{color: True},
    )
