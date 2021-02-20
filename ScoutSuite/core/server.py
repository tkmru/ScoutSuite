from flask import Flask, request, jsonify

import json # TO REMOVE
with open('/Users/noboruyoshida/code/ScoutSuite/scoutsuite-report/scoutsuite-results/scoutsuite_results_aws-186023717850.json') as json_file:
    results = json.load(json_file)


# def start_api(results):
app = Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>SCOUT SUITE WEB APP</h1>
        '''

@app.route('/api', methods=['GET'])
def api():
    return jsonify(results)

@app.route('/api/services/<service>/findings', methods=['GET'])
def get_findings(service):
    return jsonify([results['services'][service]['findings']])

@app.route('/api/services/<service>/findings/<finding>/items', methods=['GET'])
def get_items(service, finding):
    item_list = []
    finding = results['services'][service]['findings'][finding]

    if not finding['items']:
        item_list = []
    else:
        path = finding['display_path'] if finding['display_path'] else finding['path']
        attributes = get_attributes_from_path(path) # [regions, vpcs]

        for item_path in finding['items']:
            item_object = {}
            words = item_path.split('.') # [ec2, regions, us-east-1, vpcs, vpc-0190d8398f12f0340, security_groups, sg-0e584bf4e7793ea2a, default_in_use]
            words = words[:-1] if 'id_suffix' in finding and words[-1] == finding['id_suffix'] else words
            item_path_with_brackets = results['services']

            for idx in range(len(path.split('.'))):
                item_path_with_brackets = item_path_with_brackets[words[idx]]
            item = {
                'id': item_path_with_brackets['id'],
                'name': item_path_with_brackets['name'],
                'display_path': '.'.join(words[:len(path.split('.'))])
            }
            item_object['item'] = item
        
            for attribute in attributes: # regions
                attribute_id = ''
                attribute_path = []
                for idx, word in enumerate(words):
                    if word == attribute:
                        attribute_path = words[:idx + 2]
                attribute_path_with_brackets = results['services']
                for idx in range(len(attribute_path)):
                    attribute_path_with_brackets = attribute_path_with_brackets[attribute_path[idx]]
                attribute_object = {
                    'id': attribute_path_with_brackets['id'],
                    'name': attribute_path_with_brackets['name'],
                    'path': '.'.join(attribute_path)
                }
                item_object[attribute] = attribute_object
            
            item_list.append(item_object)

    return jsonify(item_list)

@app.route('/api/services/<service>/findings/<finding>/items/<item_id>', methods=['GET'])
def get_issue_paths(service, finding, item_id):
    path = request.args.get('path')
    items = results['services'][service]['findings'][finding]['items']
    issue_paths = []
    for item_path in items:
        if (path == item_path):
            issue_paths.append('THE WHOLE PATH')
        if (path in item_path):
            issue_path = item_path.split(path)[1][1:]
            issue_paths.append(issue_path)

    return { 'path_to_issues': issue_paths }

# @app.route('/api/services/', methods=['GET'])
# def get_services():
#     metadata = results['metadata']
#     category_list = []

#     for category in metadata:
#         category_id = category
#         # get category name

#         services = metadata[category]

#         for service in services:
#             service_id = service
#             # get service name

#             if 'summaries' in service[]
#             # dashboards = metadata[category][service]['resources']
#             print('category: ' + category)
#             print('service: ' + service)

#             # print(dashboards)

    
#     return jsonify(results['services'])


def get_attributes_from_path(path):
    attributes = []
    words = path.split('.')
    for idx, word in enumerate(words):
        if word == 'id':
            attributes.append(words[idx-1])

    return attributes[:-1]


# /services/{service}/findings/{finding}/items/{itemID}?path=ec2.regions.{region}.vpcs.{vpc}.security_groups.{sg_id}
# /services


app.run()
