from Notebooks.llm_model.call_model import ModelCaller


def main():
    print("This is a test file for the llm_model module.")
    model = "openai/gpt-4.1"
    print(f"Model selected: {model}\n\n ---------------------- Response ----------------------")
    obj = ModelCaller(model)
    print(obj.call_model("Tell me about Deep space?"))

if __name__ == '__main__':
    main()