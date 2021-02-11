## Blender 上での翻訳において、文字列フォーマットを利用する方法
参考1：[公式のAPI Document](https://docs.blender.org/api/current/bpy.app.translations.html#bpy.app.translations.pgettext)

参考2：[ぬっち氏の「Blenderスクリプトを多言語対応させる方法」](https://qiita.com/nutti/items/adcf4feb45135d649105)
　
 

### Blender 2.91 での結論
---------------------------
- %演算子、 `str.format()`、 f 文字列の3つとも利用可能
- 通常の場所、つまり`label(text="")`では、`bpy.app.translations.pgettext_iface()`を使う<br>
	ツールチップ(多分description)では`bpy.app.translations.pgettext_tip()`を使う<br>
	`bpy.app.translations.pgettext()`でも可能だが、公式側は推奨していない


- %演算子 ・ `str.format()`を使う方法
	- 長所：記述量が少ない
	- 短所：辞書側の記述が `"{} を削除しました"` のようになり、少し情報不足


- f 文字列を使う方法
	- 長所：`"{object.name} を削除しました"` のようになるので、結果が想像しやすい
	- 短所：必要な処理が増え、クォーテーションが多用されるのでコードが読みづらい<br>
	　　　(2行に分けて良いならば、それほど問題ではなさそう)


### 具体的な方法
----------------

- 辞書のイメージ
    1. `"Active Object is %s"`　→　`"アクティブオブジェクトは %s です"`
    2. `"Active Object is {}"`　→　`"アクティブオブジェクトは {} です"`
    3. `\'f"Active Object is {name}"\'`　→　`\'f"アクティブオブジェクトは {name} です"\'`
    4. `"Active Object is {name}"`　→　`"アクティブオブジェクトは {name} です"`
    <details><summary>実際の辞書</summary>
    
    ```python
    translation_dict = {
    	"en_US" :{
    		("*", "1: Active Object is %s") : "1: Active Object is %s",
    		("*", "2: Active Object is {}") : "2: Active Object is {}",
    		("*", 'f"3: Active Object is {name}"') : 'f"3: Active Object is {name}"',
    		("*", "4: Active Object is {name}") : "4: Active Object is {name}",
    		},
    	"ja_JP" :
    		{
    		("*", "1: Active Object is %s") : "1: アクティブオブジェクトは %s です",
    		("*", "2: Active Object is {}") : "2: アクティブオブジェクトは {} です",
    		("*", 'f"3: Active Object is {name}"') : 'f"3: アクティブオブジェクトは {name} です"',
    		("*", "4: Active Object is {name}") : "4: アクティブオブジェクトは {name} です",
    		}
    }
    ```
    注意：辞書の key と英語の翻訳先に同じテキストを設定している
    </details>


- %演算子を使う方法
```python
# 翻訳結果にフォーマットを適用するので、pgettext_iface() の外に "% (~)"を記述する
label(text = bpy.app.translations.pgettext_iface("Active Object is %s") % (context.active_object.name) )
```

- `str.format()`を使う方法
```python
# 翻訳結果にフォーマットを適用するので、pgettext_iface() の外に ".format(~)"を記述する
label(text = bpy.app.translations.pgettext_iface("Active Object is {}").format(context.active_object.name) )
```

- f 文字列を使う方法その1： f"~"を直接記述し、全体を\' \'で囲む　→　翻訳結果を`eval()`で評価
```python
# eval( 'f"名前は {name} です"' ) のようなもの。もっと良い方法があると思う
label(text = eval(
        bpy.app.translations.pgettext_iface('f"Active Object is {context.active_object.name}"' )
        )
    )
```

- f文字列を使う方法その2： f"~"は記述せず、翻訳後に追加する　→　`eval()`で評価
```python
# eval( f'f"{名前は {name} です}"' ) のようなもの。もっと良い方法が知りたい
label(text = eval(
        f'f"{bpy.app.translations.pgettext_iface("4: Active Object is {name}")}"'
        )
    )
```


### 結果
------------------------------

アドオンを読み込み、Testingタブからアドオンの詳細を表示させると、以下のような表示となる<br>
アクティブなオブジェクトを変更し、アドオンの詳細の上にマウスを動かすなどして再度 draw() を実行させると、翻訳結果も変わることが確認できるはず

![](https://github.com/nikogoli/Testing_Traslation_using_string_format/blob/main/result.png)


<details><summary>◇感想</summary>

- 手軽なのは`.format()`だが、空の"{}"が入った文章を扱いたくない
- f 文字列その1は悪くないが、f を入れ忘れる自分が想像できるのであまり使いたくない
- f 文字列その2は、2行に分ければ**記述は**整理できるが、ミスが多発しそうなのは変わらず
	```python
	text = bpy.app.translations.pgettext_iface("4: Active Object is {name}")
	self.layout.label(text = eval(f"f'{text}'"))
	```
</details>
　　　
