![covidashboard](https://socialify.git.ci/majimearun/covidashboard/image?description=1&font=KoHo&forks=1&language=1&pattern=Signal&stargazers=1&theme=Dark)

<br>

## Notes
1. The [old version](https://github.com/anandrajaram21/covidash) of the project is broken. In this repository the data is being collected using an updated data api and pipeline.
2. For a working version of the dashboard (but using old data api/pipeline) check fork of original at [covidash](https://github.com/anirudhlakhotia/covidash)
    - [Report and Screenshots of dahsboard](https://drive.google.com/file/d/1ASTxyQcch860FQVMqSMhQsaxIkiqG4pG/view?usp=sharing)
3. To just test/run notebook:
   - download [TSErrors.py](https://github.com/majimearun/covid-analysis/blob/main/src/TSErrors.py)
   - open the notebook and run it on google colab using the given linkbutton below
   - upload TSErrors.py as a utility script
   - run the notebook

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Cbt9Bj6c9-10vqdpvI6Fcbx1WmUQP6Pg?usp=sharing)


## Local environment setup (using vscode on windows):

### Using anaconda/miniconda:

- Create environment:
  ```
  conda env create -f environment.yml
  ```

- Choose new env kernel in vscode and run notebook

[Report and Screenshots of dahsboard]()