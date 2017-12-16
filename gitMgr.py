#!/usr/bin/python

import argparse
import os
from termcolor import colored

def argumentsParser():
    parser = argparse.ArgumentParser(description='Script updating/exporting GIT projects')
    parser.add_argument('-r', '--root', type=str, help='GIT projects root directory', required=True)
    parser.add_argument('-u', '--update', help='Update GIT repositories', action='store_true', required=False)  
    parser.add_argument('-s', '--skip', help='Skip user validation for updating GIT projects', action='store_true', required=False)
    parser.add_argument('-e', '--export', type=str, help='Export GIT projects URLs in a gitexport.txt', required=False)
    parser.add_argument('-d', '--download', type=str, help='Download GIT projects from URLs saved in gitexport.txt', required=False)    
    args = parser.parse_args()
    return (os.path.abspath(args.root), args.skip, args.export, args.update, args.download)

def exportGitRepositories(root, projects, filename):
    count = 0
    try:
        os.remove(filename)
    except OSError:
        pass    
    fd = open(filename, 'w+')
    for project in projects:
       os.chdir(project)        
       git_url = os.popen("git config --get remote.origin.url").read().strip('\r')
       fd.write(git_url)
       print colored('Exporting project %s' % project, 'green')
       print '\n%s\n' % ('#' * 80)
       count += 1
    fd.close()
    os.chdir(root)
    print colored('\nExport succeeded - %d projects exported' % count, 'green')

def findGitRepositories(root):
	projects = []
	for root, directories, files in os.walk(root):
		for directory in directories:
			if directory == '.git':
				git_project = os.path.join(root, directory)
				projects.append(os.path.dirname(git_project))
	return projects

def importGitRepositories(root, filename):
    count = 0
    fd = open(filename, 'r')
    projects = fd.readlines()
    for project in projects:
        print colored('Downloading project %s' % project, 'green')
        print os.popen("git clone %s" % project).read()
        count += 1
        print '\n%s\n' % ('#' * 80)
    print colored('\nDownload succeeded - %d projects downloaded' % count, 'green')

def updateGitRepository(project):
	os.chdir(project)
	print os.popen("git pull").read()

def updateGitRepositories(root, projects, skip_validation):
	for project in projects:
		project_name = os.path.basename(project)
		if skip_validation:
    			print colored('Updating project %s' % project_name, 'green')
	    		updateGitRepository(project)
    		else:
    			response = raw_input('Do you want to update project %s ? [y/n] (Default: no) : ' % (project_name))
	    		if response.lower() == 'y':
    				print colored('Updating project %s' % project_name, 'green')
    				updateGitRepository(project)
	    		else:
    				print colored('Skipping update for project %s' % project_name, 'red')
	    	os.chdir(root)
    		print '\n%s\n' % ('#' * 80)


if __name__ == '__main__':
    (root, skip_validation, export_filename, update_repositories, import_filename) = argumentsParser()
    if not os.path.exists(root):
        print colored('Directory %s does not exist' % root, 'red')
    projects = findGitRepositories(root)
    if update_repositories:
        updateGitRepositories(root, projects, skip_validation)
    if export_filename:
        exportGitRepositories(root, projects, export_filename)
    if import_filename:
        importGitRepositories(root, import_filename)
