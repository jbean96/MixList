import subprocess

def main():
    command_list = ["pandoc", "proposal.md", "--pdf-engine=xelatex", "-o", "proposal.pdf", "-V", "geometry:margin=1in"]
    print("Running: %s" % str.join(" ", command_list))
    subprocess.run(command_list)

if __name__ == '__main__':
    main()