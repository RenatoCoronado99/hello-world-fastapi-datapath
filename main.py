from fastapi import FastAPI

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Union, Optional
from constants import FAKE_DB_TOOLS

tools_list = list()
tools_list.extend(FAKE_DB_TOOLS)


class Tool(BaseModel):
    id: Optional[str] = None
    name: str
    category: str


def find_index_by_id(tool_id):
    _index = None
    for index, value in enumerate(tools_list):
        if value['id'] == tool_id:
            _index = index
            break
    return _index


app = FastAPI()


@app.get(path='/api/tools/get_all')
async def get_all_tools(category: Union[str, None] = None):
    response = tools_list
    if category:
        response = list(filter(lambda x: x['category'] == category, tools_list))
    return JSONResponse(content=response, status_code=200)


@app.get(path='/api/tools/{tool_id}')
async def get_tool(tool_id: str):
    response = None
    status_code = 404

    for tool in tools_list:
        if tool['id'] == tool_id:
            response = tool
            status_code = 200
            break

    return JSONResponse(content=response, status_code=status_code)


@app.post(path='/api/tools')
async def create_tool(tool: Tool):
    tool_id = tool.id
    if tool_id is None:
        tool.id = f'{tool.name}-{tool.category}'
    tools_list.append(tool.dict())
    json_data = jsonable_encoder(tool)
    return JSONResponse(content=json_data, status_code=201)


@app.put(path='/api/tools/{tool_id}')
async def update_tool(tool_id: str, tool: Tool):
    if tool.id is None:
        tool.id = f'{tool.name}-{tool.category}'
    index_update = find_index_by_id(tool_id=tool_id)
    if index_update is None:
        return JSONResponse(content=None, status_code=404)
    else:
        tools_list[index_update] = tool.dict()
    return JSONResponse(content=True, status_code=200)


@app.delete(path='/api/tools/{tool_id}')
async def delete_tool(tool_id: str):
    index_delete = find_index_by_id(tool_id=tool_id)
    if index_delete is None:
        return JSONResponse(content=None, status_code=404)
    else:
        tools_list.pop(index_delete)
    return JSONResponse(content=True, status_code=200)












