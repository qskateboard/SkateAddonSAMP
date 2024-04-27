local socket = require("socket")
local json = require("json")
local sampev = require("lib.samp.events")
local effil = require("effil")
local host, port = "127.0.0.1", 8888


local client = socket.tcp()
client:connect(host, port)
client:settimeout(0)

local function handleCommand(cmd, args)
    if cmd == "sendMessage" then
        sampAddChatMessage(args[1], args[2])
    end
    if cmd == "sendChat" then
        sampSendChat(args)
    end
end

function worker()
    local packet_length, packet, data
    local success, err = pcall(function()
        packet_length = client:receive(4)
        if packet_length then
            local number = tonumber(packet_length)
            if number == nil then
                print("Error: packet_length is not a number")
            else
                packet_length = number
                packet = client:receive(packet_length)
                print(packet)
                data = json.decode(packet)
            end
        end
    end)
    if success then
        if data and data.event == "command" then
            handleCommand(data.cmd, data.args)
        end
    else
        print("Error: ", err)
    end
end


function main()
    lua_thread.create(function()
        while true do
            worker()
            wait(10)
        end
    end)

    while true do
        wait(0)
    end
end

local function sendEvent(event, ...)
    local args = {...}
    local data = {event = event, args = args}
    local packet = json.encode(data)
    local packet_length = string.format("%04d", #packet)
    print(packet_length .. packet)
    client:send(packet_length .. packet)
end

function sampev.onSendChat(message)
    sendEvent("onSendChat", message)
end

function sampev.onSendCommand(command)
    print(command)
    sendEvent("onSendCommand", command)

    if command == "/skate.rec" then
        client:close()
        client = socket.tcp()
        client:connect(host, port)
        client:settimeout(0)
    end
end

function sampev.onServerMessage(color, message)
    sendEvent("onServerMessage", color, message)
end

function sampev.onShowDialog(dialogId, style, title, button1, button2, text)
    sendEvent("onShowDialog", dialogId, style, title, button1, button2, text)
end