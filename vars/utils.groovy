String slugify(String input) {
    //return input.toLowerCase().replaceAll("[^a-z0-9-]", "");
    def result = input.replaceAll('\\/','-').toLowerCase()
    result = result.replaceAll(/[^\w\s-]/, '')
    return result.replaceAll(/[-\s]+/, '-')
}

String isPrimaryBranch(String branchName) {
    if (branchName == 'main' || branchName == 'master' || branchName.startsWith('release'))
        return true
    return false
}

String getLongCommit() {
    return sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
}

def getModifiedFiles(String commit_id) {
    def output = sh (returnStdout: true, script: "git diff --name-only ${commit_id}")
    return output.tokenize('\n')
}
