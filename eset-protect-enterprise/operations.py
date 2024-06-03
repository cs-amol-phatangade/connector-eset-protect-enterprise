from connectors.core.connector import ConnectorError, get_logger
import requests
from datetime import datetime, timedelta

logger = get_logger('eset-protect-enterprise')


def make_api_call(config, url, method="GET", params=None, data=None, json_data={}):
    try:
        token = authenticate(config)
        headers = {"Authorization": token, "accept": "application/json", "Content-Type": "application/json"}
        response = requests.request(method=method, url=url,
                                    headers=headers, data=data, json=json_data, params=params, verify=config.get("verify_ssl"))
        if response.ok:
            if response.content:
                response = response.json()
            else:
                response = {"Success": "No Data Returned"}
            return response
        logger.error(response)
        raise ConnectorError(str(response))
    except Exception as e:
        if 'Max retries exceeded' in str(e):
            raise ConnectorError(
                'Max retries exceeded. Please check the URL provided for configuration of connector')
        raise ConnectorError(e)


def authenticate(config):
    try:
        username = config.get("server_username")
        password = config.get("server_password")
        base_url = config.get("base_url")
        auth_url = f"{base_url}/oauth/token"
        auth_data = {"grant_type": "password", "username": username, "password": password, "refresh_token": "refresh_token"}
        headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(auth_url, data=auth_data, headers=headers)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            logger.error("Authentication failed.")
            raise ConnectorError('Authentication failed. {}'.format(str(response)))
    except Exception as err:
        logger.exception('An exception occurred {}'.format(str(err)))
        raise ConnectorError('An exception occurred {}'.format(str(err)))


def get_executables(config, params):
    try:
        base_url = params.get("server_url")
        executableUuid = params.get("executableUuid")
        query_params = {}
        if executableUuid:
            endpoints_url = f"{base_url}/v1/executables/{executableUuid}"
        else:
            endpoints_url = f"{base_url}/v1/executables"
            if params.get("pageSize"):
                query_params.update({"pageSize": params.get("pageSize")})
            if params.get("pageToken"):
                query_params.update({"pageToken": params.get("pageToken")})
        return make_api_call(config, endpoints_url, params=query_params)
    except Exception as err:
        logger.exception('Failed to get all executables {}'.format(str(err)))
        raise ConnectorError('Failed to get all executables {}'.format(str(err)))


def block_unblock_executables(config, params, action):
    try:
        base_url = params.get("server_url")
        executableUuid = params.get("executableUuid")
        endpoints_url = f"{base_url}/v1/executables/{executableUuid}:{action}"
        data = params.get("json_data", {})
        return make_api_call(config, endpoints_url, data=data)
    except Exception as err:
        logger.exception('Failed to block/unblock executables {}'.format(str(err)))
        raise ConnectorError('Failed to block/unblock executables {}'.format(str(err)))


def block_executables(config, params):
    return block_unblock_executables(config, params, "block")


def unblock_executables(config, params):
    return block_unblock_executables(config, params, "unblock")


def get_device(config, params):
    try:
        base_url = params.get("server_url")
        deviceUuid = params.get("deviceUuid")
        endpoints_url = f"{base_url}/v1/devices/{deviceUuid}"
        return make_api_call(config, endpoints_url)
    except Exception as err:
        logger.exception('Failed to get device. {}'.format(str(err)))
        raise ConnectorError('Failed to get device. {}'.format(str(err)))


def get_device_group(config, params):
    try:
        base_url = params.get("server_url")
        groupUuid = params.get("groupUuid")
        query_params = {}
        if groupUuid:
            endpoints_url = f"{base_url}/v1/device_groups/{groupUuid}/devices"
        else:
            endpoints_url = f"{base_url}/v1/device_groups"
        if params.get("pageSize"):
            query_params.update({"pageSize": params.get("pageSize")})
        if params.get("pageToken"):
            query_params.update({"pageToken": params.get("pageToken")})
        return make_api_call(config, endpoints_url, params=query_params)
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def get_detections(config, params):
    try:
        base_url = params.get("server_url")
        detectionUuid = params.get("detectionUuid")
        query_params = {}
        if detectionUuid:
            endpoints_url = f"{base_url}/v1/detections/{detectionUuid}"
        else:
            endpoints_url = f"{base_url}/v1/detections"
            if params.get("deviceUuid"):
                query_params.update({"deviceUuid": params.get("deviceUuid")})
            if params.get("start_time"):
                query_params.update({"startTime": params.get("start_time")})
            if params.get("end_time"):
                query_params.update({"endTime": params.get("end_time")})
            if params.get("pageSize"):
                query_params.update({"pageSize": params.get("pageSize")})
            if params.get("pageToken"):
                query_params.update({"pageToken": params.get("pageToken")})
        return make_api_call(config, endpoints_url, params=query_params)
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def get_detection_groups(config, params):
    try:
        base_url = params.get("server_url")
        detectionGroupUuid = params.get("detectionGroupUuid")
        query_params = {}
        if detectionGroupUuid:
            endpoints_url = f"{base_url}/v2/detection-groups/{detectionGroupUuid}"
        else:
            endpoints_url = f"{base_url}/v2/detection-groups"
            if params.get("deviceUuid"):
                query_params.update({"deviceUuid": params.get("deviceUuid")})
            if params.get("start_time"):
                query_params.update({"startTime": params.get("start_time")})
            if params.get("end_time"):
                query_params.update({"endTime": params.get("end_time")})
            if params.get("pageSize"):
                query_params.update({"pageSize": params.get("pageSize")})
            if params.get("pageToken"):
                query_params.update({"pageToken": params.get("pageToken")})
        return make_api_call(config, endpoints_url, params=query_params)
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def get_device_tasks(config, params):
    try:
        base_url = params.get("server_url")
        endpoints_url = f"{base_url}/v1/device_tasks"
        query_params = {}
        if params.get("pageSize"):
            query_params.update({"pageSize": params.get("pageSize")})
        if params.get("pageToken"):
            query_params.update({"pageToken": params.get("pageToken")})
        return make_api_call(config, endpoints_url, params=query_params)
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def isolate_computer_from_network(config, params):
    try:
        base_url = params.get("server_url")
        endpoints_url = f"{base_url}/v1/device_tasks"
        task_expire_time = params.get("task_expire_time")
        current_time = datetime.now()
        new_time = current_time + timedelta(minutes=task_expire_time)
        formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        isolation_device = {
            "task": {
            "description": params.get("device_uuid", "IsolateDeviceASAP"),
            "displayName": params.get("device_uuid", "IsolateDevice"),
            "targets": {
                 "devicesUuids": [params.get("device_uuid")],
                 "deviceGroupsUuids": [params.get("device_group_uuid")]
            },
            "triggers": [{
                 "manual": {
                         "expireTime": formatted_time
                }
            }],
            "action": {
                 "name": "StartNetworkIsolation"
                }
            }
        }
        params.get("device_uuid")
        return make_api_call(config, endpoints_url, json_data=isolation_device, method="POST")
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def end_computer_isolation_from_network(config, params):
    try:
        base_url = params.get("server_url")
        endpoints_url = f"{base_url}/v1/device_tasks"
        task_expire_time = params.get("task_expire_time")
        current_time = datetime.now()
        new_time = current_time + timedelta(minutes=task_expire_time)
        formatted_time = new_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        isolation_device = {
            "task": {
            "description": params.get("device_uuid", "IsolateDeviceASAP"),
            "displayName": params.get("device_uuid", "IsolateDevice"),
            "targets": {
                 "devicesUuids": [params.get("device_uuid")],
                 "deviceGroupsUuids": [params.get("device_group_uuid")]
            },
            "triggers": [{
                 "manual": {
                         "expireTime": formatted_time
                }
            }],
            "action": {
                 "name": "EndNetworkIsolation"
                }
            }
        }
        params.get("device_uuid")
        return make_api_call(config, endpoints_url, json_data=isolation_device, method="POST")
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


def create_device_tasks(config, params):
    try:
        base_url = params.get("server_url")
        endpoints_url = f"{base_url}/v1/device_tasks"
        task_payload = params.get("task_payload")
        return make_api_call(config, endpoints_url, json_data=task_payload, method="POST")
    except Exception as err:
        logger.exception('Failed to get device group. {}'.format(str(err)))
        raise ConnectorError('Failed to get device group. {}'.format(str(err)))


operations_map = {
    'get_executables': get_executables,
    'block_executables': block_executables,
    'unblock_executables': unblock_executables,
    'get_device': get_device,
    'get_device_group': get_device_group,
    'get_detections': get_detections,
    'get_detection_groups': get_detection_groups,
    'get_device_tasks': get_device_tasks,
    'isolate_computer_from_network': isolate_computer_from_network,
    'create_device_tasks': create_device_tasks,
    'end_computer_isolation_from_network': end_computer_isolation_from_network
}
