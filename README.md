### What is each file?

- `store.yaml`: this file is used to write commits. it also show the commit frequency per day, but this is not used as a source of truth, and will be overwritten by the data from `git log`.

### How to run

1. Install required dependencies

```
pip install -r requirements.txt
```

2. Run python script with arguments
   - `-f <filename>` to reference html file
   - `-u <url>` to reference a url

```
python main.py -u "https://github.com/user"
```

3. Push Commits

```
git push
```

4. If your repo is private, turn on visibility in settings

<!-- show SS of setting -->
