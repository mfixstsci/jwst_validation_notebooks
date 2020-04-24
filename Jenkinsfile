pipeline {
  agent { label 'linux' }

  environment {
    env_name = "jwst_validation_notebooks"
    deploy_branch = "gh-pages"
    HOME="${WORKSPACE}"
    TEST_BIGDATA="https://bytesalad.stsci.edu/artifactory"
    CRDS_SERVER_URL = "https://jwst-crds.stsci.edu"
    CRDS_PATH = "/tmp/crds_cache"
    PATH ="${WORKSPACE}/miniconda3/bin:${PATH}"
    TMPDIR="${WORKSPACE}/tmp"
    XDG_CACHE_HOME="${WORKSPACE}/tmp/.cache"
  }

  stages {
    stage('Setup') {
      steps {
        deleteDir()
        checkout scm
        sh("mkdir -p tmp")
        sh("curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -o installer.sh")
        sh("bash installer.sh -b -p ${WORKSPACE}/miniconda3")
        sh("curl -LO https://raw.githubusercontent.com/astroconda/docker-buildsys/master/with_env")
        sh("chmod +x with_env")
        sh("conda create -n ${env_name} python=3.7 git -y")
        sh("./with_env -n ${env_name} pip install -r requirements.txt")
      }
    }

    stage('Convert/Check') {
      steps {
        sh("./with_env -n ${env_name} python convert.py --report report.txt")
        sh("./with_env -n ${env_name} python -m 'nbpages.check_nbs' --notebook_path jwst_validation_notebooks")
      }
    }

    stage('Deploy') {
      steps {
        script {
          if(env.JOB_NAME.toLowerCase().contains('pr')) {
            echo "Pull Request, Not deploying..."
          } else {
            echo "Deploying to Github Pages"
              sshagent (credentials: ['mfixstsci-jwst_validation_notebooks']) {
                // TODO: Update url (ssh url for repo)
                sh("git clone -b ${deploy_branch} --single-branch git@github.com:mfixstsci/jwst_validation_notebooks.git notebooks_clone")
                dir('./notebooks_clone') {
                  sh("""cp -aR ${env.WORKSPACE}/jwst_validation_notebooks/* ./jwst_validation_notebooks/
                    cp ${env.WORKSPACE}/index.html ./index.html
                    git config --global user.email jenkins-deploy@stsci.edu
                    git config --global user.name jenkins-deploy
                    git status
                    git add .
                    git commit -m 'Automated deployment to GitHub Pages: ${env.BUILD_TAG}' --allow-empty
                    git push origin ${deploy_branch}
                    rsync -avzH ./index.html ${env.WEBPAGE_DIR}
                    rsync -avzHR ./jwst_validation_notebooks/*/*/*.html ${env.WEBPAGE_DIR}
                    """
                    )
                }
              }
              deleteDir()
          }
        } // end of script
      } // end of deploy steps
    } // end of deploy stage
  } // end of stages
  post {
        cleanup { 
            deleteDir()
        } //end of cleanup
  } //end of post
} // end of pipeline