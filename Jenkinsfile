def sourceInfo = null
try {
    println("Attempting to load shared lib from branch: ${env.BRANCH_NAME}")
    if ("${TOOLS_URL}".contains('git'))
        sourceInfo = [$class: 'GitSCMSource', remote: "${TOOLS_URL}"]
    else
        sourceInfo = [$class: 'GitSCMSource', remote: "${TOOLS_URL}", credentialsId: "tenant-bitbucket-ro-cred"]

    library identifier: "jenkins-shared-lib@${BRANCH_NAME}", retriever: modernSCM(sourceInfo)
} catch (err) {
    println("Problem using BRANCH_NAME variable, trying main")
    library identifier: "jenkins-shared-lib@main", retriever: modernSCM(sourceInfo)
}

podTemplates.pythonTemplate {
    node(POD_LABEL) {
        def params = [:]
        String slugBranchName = utils.slugify(env.BRANCH_NAME)

        println("Branch Name: ${env.BRANCH_NAME} -- Branch Name(Slug): ${slugBranchName}")

        stage('Clone code') {
            checkout scm
        }

        stage('Build Config')
        {
            println("Executing command in python3 container")
            container('python')
            {
                sh '''
                    python3 -m pip install PyYAML && \
                    python3 config/build_config.py
                   '''
            }

            sh 'cat config/config.yaml'
        }

        // TODO: Remove when vault is integrated
        withCredentials([usernamePassword(credentialsId: 'bitbucket-plugin-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
            stage('Job DSL') {
                try {
                    Map configYaml = readYaml (file: 'config/config.yaml')
                    boolean isPrimaryBranch = utils.isPrimaryBranch(env.BRANCH_NAME)
                    String pathTestingRoot = 'job-testing'

                    params = [ 'isPrimaryBranch' : isPrimaryBranch,
                               'rootJobTesting' : pathTestingRoot,
                               'pathPrefix' : getPathPrefix(isPrimaryBranch, getPathPrefix, env.BRANCH_NAME),
                               'configYaml' : configYaml,
                               'branchName' : env.BRANCH_NAME,
                               'branchNameSlug' : utils.slugify(env.BRANCH_NAME),
                               'pathWorkspace' : env.WORKSPACE,
                               'urlTools' : env.TOOLS_URL,
                               'passwordBootstrap' : env.PASSWORD ]
                    //'dsl/createTenantRoot.groovy'
                    jobDsl targets: [   'dsl/createTestingRoot.groovy',


                                        ].join('\n'),
                            removedJobAction: 'DELETE',
                            removedViewAction: 'DELETE',
                            lookupStrategy: 'JENKINS_ROOT',
                            additionalParameters: params
                }
                catch (Exception ex) {
                    println("Exception: ${ex.toString()}")
                    sh('exit 1')
                }
            }
        }
    }
}

