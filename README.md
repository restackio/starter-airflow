# Airflow Restack repository

This is the default Airflow repository to get you started for generating preview environments from a custom airflow image with Restack github application.

### Dags
1. If you want to extend the image with custom dags, just add them to the dags directory.

### Plugins

1. If you want to extend the image with custom plugins, just add them to the plugins directory.

### Config

1. If you want to extend the image with custom configuration, just add them to the config directory.


### Generating a preview environment.
1. Make sure to fork this repository.
2. Follow steps in the [official Restack documentation](https://www.restack.io/docs/airflow-ci-cd)
3. Once you open a pull request a preview environment will be generated.
4. Once your pull request is merged your initial airflow application will be provisioned with latest code from the "main" branch.
