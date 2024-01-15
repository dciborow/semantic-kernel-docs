async def main():
    import semantic_kernel as sk
    from semantic_kernel.core_skills import ConversationSummarySkill
    import config.add_completion_service

    # Initialize the kernel
    kernel = sk.Kernel()
    # Add a text or chat completion service using either:
    # kernel.add_text_completion_service()
    # kernel.add_chat_service()
    kernel.add_completion_service()

    # Import the ConversationSummaryPlugin
    kernel.import_skill(
        ConversationSummarySkill(kernel=kernel), skill_name="ConversationSummaryPlugin"
    )

    # Import the OrchestratorPlugin from the plugins directory.
    prompts = kernel.import_semantic_skill_from_directory(".", "prompts")

    # Create the history
    history = []

    while True:
        request = input("User > ")

        variables = sk.ContextVariables()
        variables["request"] = request
        variables["history"] = "\n".join(history)

        # Run the prompt
        result = await kernel.run_async(
            prompts["chat"],
            input_vars=variables,
        )

        history.extend((f"User: {request}", f"Assistant{result.result}"))
        print(f"Assistant > {result.result}")


# Run the main function
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
