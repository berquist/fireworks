__author__ = 'Morgan Hargrove'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Morgan Hargrove'
__email__ = 'mhargrove@lbl.gov'
__date__ = 'Jun 13, 2013'

import json
from pymongo import DESCENDING
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from fireworks.core.launchpad import LaunchPad
from fireworks.utilities.fw_serializers import DATETIME_HANDLER

lp = LaunchPad() # LaunchPad.auto_load()

def home(request):
    shown = 9
    # Newest Fireworks table data
    fws_shown = lp.get_fw_ids(limit=shown, sort=[('created_on', DESCENDING)])
    fw_names = []
    fw_states = []
    for fw in fws_shown:
        fw_names.append(lp.get_fw_by_id(fw).name)
        fw_states.append(lp.get_fw_by_id(fw).state)
    fw_info = zip(fws_shown, fw_names, fw_states)

    # Current Database Status table data
    states = ['ARCHIVED', 'DEFUSED', 'WAITING', 'READY', 'RESERVED',
        'FIZZLED', 'RUNNING', 'COMPLETED']
    fw_nums = []
    wf_nums = []
    for state in states:
        fw_nums.append(lp.get_fw_ids(query={'state': state}, count_only=True))
        wf_nums.append(lp.get_wf_ids(query={'state': state}, count_only=True))
    tot_fws   = lp.get_fw_ids(count_only=True)
    tot_wfs   = lp.get_wf_ids(count_only=True)
    info = zip(states, fw_nums, wf_nums)

    # Newest Workflows table data
    wfs_shown = lp.get_wf_ids(limit=shown, sort=[('created_on', DESCENDING)])
    wf_names = []
    wf_states = []
    for wf in wfs_shown:
        wf_names.append(lp.get_wf_by_fw_id(wf).name)
        wf_states.append(lp.get_wf_by_fw_id(wf).state)
    wf_info = zip(wfs_shown, wf_names, wf_states)

    return render_to_response('home.html', {'fw_info': fw_info, 'wf_info': wf_info,
        'info': info, 'tot_fws': tot_fws, 'tot_wfs': tot_wfs})

def fw(request):
    fws = lp.get_fw_ids(count_only=True)
    shown = 20
    fws_shown = lp.get_fw_ids(limit=shown, sort=[('created_on', DESCENDING)])
    fw_names = []
    fw_states = []
    for fw in fws_shown:
        fw_names.append(lp.get_fw_by_id(fw).name)
        fw_states.append(lp.get_fw_by_id(fw).state)
    fw_info = zip(fws_shown, fw_names, fw_states)
    return render_to_response('fw.html', {'fws': fws, 'fw_info': fw_info})

def fw_state(request, state):
    fws = lp.get_fw_ids(query={'state': state}, count_only=True)
    shown = 20
    fws_shown = lp.get_fw_ids(limit=shown, sort=[('created_on', DESCENDING)], query={'state': state})
    fw_names = []
    for fw in fws_shown:
        fw_names.append(lp.get_fw_by_id(fw).name)
    fw_info = zip(fws_shown, fw_names)
    return render_to_response('fw_state.html', {'fws': fws, 'state': state, 'fw_info': fw_info})

def fw_id(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    fw = lp.get_fw_by_id(id)
    fw_dict = fw.to_dict()
    if 'archived_launches' in fw_dict:
        del fw_dict['archived_launches']
    del fw_dict['spec']
    fw_data = json.dumps(fw_dict, default=DATETIME_HANDLER, indent=4)
    return render_to_response('fw_id.html', {'fw_id': id, 'fw_data': fw_data})

def fw_id_all(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    fw = lp.get_fw_by_id(id)
    fw_data = json.dumps(fw.to_dict(), default=DATETIME_HANDLER, indent=4)
    return render_to_response('fw_id.html', {'fw_id': id, 'fw_data': fw_data})

def fw_id_less(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    fw = lp.get_fw_by_id(id)
    fw_dict = fw.to_dict()
    if 'archived_launches' in fw_dict:
        del fw_dict['archived_launches']
    del fw_dict['spec']
    if 'launches' in fw_dict:
        del fw_dict['launches']
    fw_data = json.dumps(fw_dict, default=DATETIME_HANDLER, indent=4)
    return render_to_response('fw_id.html', {'fw_id': id, 'fw_data': fw_data})

def wf(request):
    wfs = lp.get_wf_ids(count_only=True)
    shown = 20
    wfs_shown = lp.get_wf_ids(limit=shown, sort=[('created_on', DESCENDING)])
    wf_names = []
    wf_states = []
    for wf in wfs_shown:
        wf_names.append(lp.get_wf_by_fw_id(wf).name)
        wf_states.append(lp.get_wf_by_fw_id(wf).state)
    wf_info = zip(wfs_shown, wf_names, wf_states)
    return render_to_response('wf.html', {'wfs': wfs, 'wf_info': wf_info})

def wf_state(request, state):
    wfs = lp.get_wf_ids(query={'state': state}, count_only=True)
    shown = 20
    wfs_shown = lp.get_wf_ids(limit=shown, sort=[('created_on', DESCENDING)], query={'state': state})
    wf_names = []
    for wf in wfs_shown:
        wf_names.append(lp.get_wf_by_fw_id(wf).name)
    wf_info = zip(wfs_shown, wf_names)
    return render_to_response('wf_state.html', {'wfs': wfs, 'state': state, 'wf_info': wf_info})

def wf_id(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    wf = lp.get_wf_by_fw_id(id)
    wf_dict = wf.to_display_dict()
    del wf_dict['name']
    del wf_dict['parent_links']
    del wf_dict['nodes']
    del wf_dict['links']
    del wf_dict['metadata']
    del wf_dict['states_list']
    wf_data = json.dumps(wf_dict, default=DATETIME_HANDLER, indent=4)
    return render_to_response('wf_id.html', {'wf_id': id, 'wf_data': wf_data})

def wf_id_all(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    wf = lp.get_wf_by_fw_id(id)
    wf_dict = wf.to_display_dict()
    del wf_dict['states_list']
    wf_data = json.dumps(wf_dict, default=DATETIME_HANDLER, indent=4)
    return render_to_response('wf_id.html', {'wf_id': id, 'wf_data': wf_data})

def wf_id_less(request, id):
    try:
        id = int(id)
    except ValueError:
        raise Http404()
    wf = lp.get_wf_by_fw_id(id)
    wf_dict = wf.to_display_dict()
    del wf_dict['name']
    del wf_dict['parent_links']
    del wf_dict['nodes']
    del wf_dict['links']
    del wf_dict['metadata']
    del wf_dict['states']
    del wf_dict['launch_dirs']
    del wf_dict['updated_on']
    wf_data = json.dumps(wf_dict, default=DATETIME_HANDLER, indent=4)
    return render_to_response('wf_id.html', {'wf_id': id, 'wf_data': wf_data})

def testing(request):
    arc_fws   = lp.get_fw_ids(query={'state':'ARCHIVED'}, count_only=True)
    def_fws   = lp.get_fw_ids(query={'state':'DEFUSED'}, count_only=True)
    wait_fws  = lp.get_fw_ids(query={'state':'WAITING'}, count_only=True)
    ready_fws = lp.get_fw_ids(query={'state':'READY'}, count_only=True)
    res_fws   = lp.get_fw_ids(query={'state':'RESERVED'}, count_only=True)
    fizz_fws  = lp.get_fw_ids(query={'state':'FIZZLED'}, count_only=True)
    run_fws   = lp.get_fw_ids(query={'state':'RUNNING'}, count_only=True)
    comp_fws  = lp.get_fw_ids(query={'state':'COMPLETED'}, count_only=True)
    tot_fws   = lp.get_fw_ids(count_only=True)
    return render_to_response('testing.html', {'arc_fws': arc_fws, 'def_fws': def_fws,
        'wait_fws': wait_fws, 'ready_fws': ready_fws, 'res_fws': res_fws,
        'fizz_fws': fizz_fws, 'run_fws': run_fws, 'comp_fws': comp_fws, 'tot_fws': tot_fws})