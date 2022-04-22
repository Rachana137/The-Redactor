# CHANGES

## Output files not stored in respective folder

For this I added a code so that it can store in the given input folder.
```bash
  def output(data, file, path):
    filepath = os.path.join(os.getcwd(), path)
    try:
        os.makedirs(filepath, exist_ok=True)
        fpath = ('%s.redacted' % (file))
        with open(os.path.join(filepath, fpath), 'w+', encoding='utf-8') as f:
            f.write(data)
            f.close()
    except OSError as error:
        print(error)
```
Here, os.makedirs() helps us to create the given folder. 

## File names not re-assigned correctly

Before changes, my files stored as "redacted_file3.txt". So I made small changes in my code.
```bash
  fpath = ('%s.redacted' % (file))
```
This line of code helps in storing the redacted file in "<file>.redacted" form. (ex. file1.txt.redacted).
