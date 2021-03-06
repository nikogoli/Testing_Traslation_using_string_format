## Blender 上での翻訳において、文字列フォーマットを利用する方法
参考1：[公式のAPI Document](https://docs.blender.org/api/current/bpy.app.translations.html#bpy.app.translations.pgettext)

参考2：[ぬっち氏の「Blenderスクリプトを多言語対応させる方法」](https://qiita.com/nutti/items/adcf4feb45135d649105)
　
 

### Blender 2.91 での結論
---------------------------
- %演算子、 `str.format()`、 f 文字列の3つとも利用可能
- 通常の場所、つまり`label(text="")`では、`bpy.app.translations.pgettext_iface()`を使う<br>
	ツールチップ(多分description)では`bpy.app.translations.pgettext_tip()`を使う<br>
	`bpy.app.translations.pgettext()`でも可能だが、公式側は推奨していない

- %演算子や `str.format()`を使う方法
	```python
	# 辞書のイメージ(%演算子)： "Active Object is %s"　→　"アクティブオブジェクトは %s です"
	# 　　　　　　(format())： "Active Object is {}"　→　"アクティブオブジェクトは {} です"
	
	# 翻訳結果にフォーマットを適用するので、pgettext_iface() の外に "% (~)" や ".format(~)"を記述する
	label(text = bpy.app.translations.pgettext_iface("Active Object is %s") % (context.active_object.name) )
	label(text = bpy.app.translations.pgettext_iface("Active Object is {}").format(context.active_object.name) )
	```
	- 長所：記述量が少ない
	- 短所：辞書側の記述が `"{} を削除しました"` のようになり、少し情報不足


- f 文字列を使う方法
	- その1： 'f"{~}"'のように f を含めて文章を翻訳(置換)し、`eval()`を使ってf 文字列として評価する
	- その2：　"{~}"のように f は含めず文章を翻訳(置換)し、f を追加した上で`eval()`で評価を使ってf 文字列として評価する
	```python
	# 辞書のイメージ(その1)： 'f"Active Object is {name}"'　→　'f"アクティブオブジェクトは {name} です"'
	# 　　　　　　　(その2)： "Active Object is {name}"　→　"アクティブオブジェクトは {name} です"
	
	# その1  eval( 'f"名前は {name} です"' ) のようなもの
	label(text = eval(
		bpy.app.translations.pgettext_iface('f"Active Object is {context.active_object.name}"' )
		))
	
	# その2  eval( f'f"{名前は {name} です}"' ) のようなもの
	label(text = eval(
		f'f"{ bpy.app.translations.pgettext_iface("Active Object is {name}") }"'
		))
	```
	- 長所：`"{object.name} を削除しました"` のようになるので、結果が想像しやすい
	- 短所：必要な処理が増え、クォーテーションが多用されるのでコードが読みづらい



### 結果
------------------------------

アドオンを読み込み、Testingタブからアドオンの詳細を表示させると、以下のような表示となる<br>
アクティブなオブジェクトを変更し、アドオンの詳細の上にマウスを動かすなどして再度 draw() を実行させると、翻訳結果も変わることが確認できるはず

<details><summary>◇仕組みの自分なりの理解</summary>

- 文字列フォーマットを直接使った場合：<br>
「英文に対応する日本語」の取得よりも前に、英語文章に対してフォーマットが適用されてしまう<br>
 　`"Object is {name}"　→　フォーマット適用　→　"Object is Cube"　→　対応する日本語の取得に失敗する(訳されない)`
 
- `pgettext_iface()`を経由した場合：<br>
  「英文に対応する日本語」の取得が先に行われるので、日本語文章に対してフォーマットを適用できる<br>
 　`"Object is {name}"　→　"オブジェクトは {name} です"　→　フォーマット適用　→　"オブジェクトは Cube です"`
</details>

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
　　　
