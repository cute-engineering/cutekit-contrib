import os
from cutekit import model, cli, builder, rules


@cli.command("f", "flag", "Generate flags for C/C++ compiler")
def flagCmd(args: cli.Args):
    tool = args.consumeOpt("tool", "cc")

    registry = model.Registry.use(args)
    target = model.Target.use(args)

    if tool not in target.tools:
        raise Exception(f"Target {target.name} does not have tool {tool}")

    arguments = target.tools[tool].args

    flags = []
    if tool in ["cc", "cxx"]:
        flags += list(
            builder.aggregateCincs(target, registry)
            | builder.aggregateCdefs(target)
            | set(rules.rules[tool].args)
        )

    i = 0
    while i < len(arguments):
        if "mcmode" in arguments[i]:
            pass
        elif "-target" in arguments[i]:
            i += 1
        else:
            flags.append(arguments[i])
        i += 1

    with open(os.path.join(registry.project.dirname(), "compile_flags.txt"), "w") as f:
        f.write("\n".join(flags))
        f.write("\n")
