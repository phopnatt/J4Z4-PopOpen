getgenv().configs = {
    ["Enablelog"] = true,   -- เปิด/ปิดการยิง heartbeat
    ["BeatEvery"] = 5,      -- ยิงทุกกี่วิ (ต้องน้อยกว่า BEAT_TIMEOUT ฝั่ง Python)
    ["Port"]      = 8000,   -- ต้องตรงกับ PORT ใน Core/accountcontrolCLI.py
}

-- executor แต่ละตัวชื่อฟังก์ชัน request ไม่เหมือนกัน กันไว้ทุกแบบ
local req = request or http_request or (syn and syn.request)
local HttpService = game:GetService("HttpService")

-- รอเกมโหลดเสร็จก่อน (auto execute ชอบรันก่อน LocalPlayer จะมา)
if not game:IsLoaded() then
    game.Loaded:Wait()
end
local player = game:GetService("Players").LocalPlayer
while not player do
    task.wait(1)
    player = game:GetService("Players").LocalPlayer
end

if getgenv().configs["Enablelog"] and req then
    while task.wait(getgenv().configs["BeatEvery"]) do
        -- pcall กันไว้ ถ้า CLI ปิดอยู่ request จะ error แต่ loop ต้องไม่ตาย
        pcall(function()
            req({
                Url = "http://127.0.0.1:" .. getgenv().configs["Port"] .. "/beat",
                Method = "POST",
                Headers = { ["Content-Type"] = "application/json" },
                Body = HttpService:JSONEncode({
                    name  = player.Name,    -- บอกว่าใครยิงมา
                    place = game.PlaceId,   -- อยู่ place ไหน (ให้ auto relaunch ส่งกลับถูกที่)
                    job   = game.JobId,     -- อยู่ server ไหน (เผื่อใช้ในอนาคต)
                }),
            })
        end)
    end
end
