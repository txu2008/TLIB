# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/8/8 12:49
# @Author  : Tao.Xu
# @Email   : tao.xu2008@outlook.com

"""
Library for jenkins.

You can use Jenkins to access your jenkins server easily.

This library uses defensive programming with EAFP principle.
Kinds of exceptions based on jenkins.Error may be raise.
You should use this library with try ... except.

usage:
::
    import tlib
    import tlib.jenkinslib

    ############### quick start ###############
    jenkins = tlib.jenkinslib.Jenkins('tlib.jenkins.baidu.com')

    job = jenkins['tlib_quick']
    print job.name, job.last_stable_build_number, job.description
    print job[5], job["lastSuccessBuild"], job.last_stable_build

    qi = job.invoke()
    build = qi.block_until_building()
    print build.name, build.number, build.timestamp

    try:
        build.block_until_complete(timeout=20)
    except tlib.jenkinslib.RunTimeout as err:
        print "timeout:", err
        build.stop()

    print build.duration, build.result, build.description

    build.description = "new description"

    jenkins.enable_ftp('ftp.baidu.com', 'tlib', 'password', 22)
    with build.ftp_artifacts as af:
        af['artifacts_path'].download('./local_path')
"""

import os
from libs.jenkinslib import internal
from libs.jenkinslib.internal import exception as _exception
from libs.jenkinslib.internal import jenkins as _jenkins
from libs.jenkinslib.internal import promotion as _promotion

# import Jenkins and Promotion
Jenkins = _jenkins.Jenkins
Promotion = _promotion.Promotion

# import exceptions
Error = _exception.Error
NotRunningOnJenkins = _exception.NotRunningOnJenkins
BadParam = _exception.BadParam
ParamTypeError = _exception.ParamTypeError
BadValue = _exception.BadValue
RunTimeout = _exception.RunTimeout
NotFound = _exception.NotFound
UnknownNode = _exception.UnknownNode
UnknownJob = _exception.UnknownJob
UnknownPromotion = _exception.UnknownPromotion
UnknownQueueItem = _exception.UnknownQueueItem
NotBuiltYet = _exception.NotBuiltYet
NoBuildData = _exception.NoBuildData
DeletedBuild = _exception.DeletedBuild
NoArtifacts = _exception.NoArtifacts
JenkinsAPIError = _exception.JenkinsAPIError
UnsupportedAPI = _exception.UnsupportedAPI
NotStopYet = _exception.NotStopYet
ImappropriateMethod = _exception.ImappropriateMethod
ImappropriateMethodInStaticMode = _exception.ImappropriateMethodInStaticMode
NotImplementedMethod = _exception.NotImplementedMethod
OSIOError = _exception.OSIOError
RequestError = _exception.RequestError
PostRequired = _exception.PostRequired
InvalidRequestStatus = _exception.InvalidRequestStatus
UnauthorizedError = _exception.UnauthorizedError
NetworkError = _exception.NetworkError
FtpError = _exception.FtpError


def get_jenkins_obj_by_url(url, username=None, password=None):
    """get Jenkins object by url.

    Args:
        url: jenkins url.
        username: username to login jenkins.
        password: password or API token of username.

    Returns:
        Jenkins object.
    """
    if not url.startswith("http"):
        url = "http://%s" % url

    params = {}
    if username is not None:
        params["username"] = username
        params["password"] = password

    cls = Jenkins.get_jenkins_by_url(url)
    return cls(url, **params)


def current_jenkins(username=None, password=None):
    """get Jenkins object of current jenkins server if running on jenkins, otherwise None.

    Current environment is recognized as jenkins env,
    if and only if all the environment variable below exists.
        JENKINS_URL
    I will get them using os.getenv.

    Args:
        username: username to login jenkins.
        password: password or API token of username.

    Returns:
        Jenkins object.
    """
    url = os.getenv("JENKINS_URL")
    if url is None:
        raise NotRunningOnJenkins()

    return get_jenkins_obj_by_url(url, username, password)


def current_job(username=None, password=None):
    """get Job object of current job if running on jenkins, otherwise None.

    Current environment is recognized as jenkins env,
    if and only if all the environment variable below exists.
        JENKINS_URL
        JOB_NAME
    I will get them using os.getenv.

    Args:
        username: username to login jenkins.
        password: password or API token of username.

    Returns:
        Job object.
    """
    job_name = os.getenv("JOB_NAME")
    if job_name is None:
        raise NotRunningOnJenkins()

    return current_jenkins(username=username, password=password)[job_name]


def current_build(username=None, password=None):
    """get Build object of current build if running on jenkins, otherwise None.

    Current environment is recognized as jenkins env,
    if and only if all the environment variable below exists.
        JENKINS_URL
        JOB_NAME
        BUILD_NUMBER
    I will get them using os.getenv.

    Args:
        username: username to login jenkins.
        password: password or API token of username.

    Returns:
        Build object.
    """
    build_number = os.getenv("BUILD_NUMBER")
    if build_number is None or not build_number.isdigit():
        raise NotRunningOnJenkins()

    return current_job(username=username, password=password)[int(build_number)]


def is_accessible(url, username, password):
    """is able to access jenkins with this password or not.

    Args:
        url: jenkins url.
        username: username to login jenkins.
        password: password or API token of username.

    Returns:
        bool.
    """
    if not url.startswith("http"):
        url = "http://%s" % url

    url = Jenkins.python_api_url(url)
    requester = Jenkins.Requester(username, password)
    try:
        response = requester.get(url)
        if response.status_code in (401, 403):
            return False
    except Error:
        return False

    return True


__all__ = ["Jenkins"]
