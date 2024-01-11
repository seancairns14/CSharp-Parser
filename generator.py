from markdowngenerator import MarkdownGenerator

def main(text):
    with MarkdownGenerator(
        filename="example.md", enable_write=False
    ) as doc:
        doc.writeTextLine("```csharp")  # Start of C# code block
        doc.writeTextLine(text)  # Writing the code content
        doc.writeTextLine("[Link to Page1](Folder1/Page1.md)")  # Reference as plain text
        doc.writeTextLine("```")  # End of C# code block

if __name__ == "__main__":
    with open('Plugin.cs', 'r') as file:
        main(file.read())
